from fastapi import FastAPI, Depends,HTTPException,status,Response,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import text,select
from passlib.context import CryptContext
from typing import Annotated 
from pydantic import BaseModel,EmailStr
from datetime import datetime, timedelta,timezone
from jose import  jwt,JWTError,ExpiredSignatureError
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import os
from src.models import models
from src.s3_utils import upload_file, download_file, s3
from src.auth_bearer import decode_jwt, JwtBearer
from src.database import engine,sessionLocal,public_base,schema_base
from src.migrate_tenants import migrate_tenant_schema
import re
import secrets
import hashlib
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()
access_key = os.getenv("SECRET_KEY")
refresh_key = os.getenv("REFRESH_KEY")
algo = os.getenv("SECRET_ALGORITHM")

""" @asynccontextmanager
async def lifespan(app: FastAPI):
    models.public_base.metadata.create_all(bind = engine)
    models.schema_base.metadata.create_all(bind = engine)
    yield """

app = FastAPI(debug=True)

origins = [
    "http://localhost:8000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_global_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_global_db)]
oauth_dependency = Annotated[OAuth2PasswordRequestForm,Depends()]
my_context = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])

def get_current_schema(request: Request, db: db_dependency):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = auth_header.split(" ")[1]
    payload = decode_jwt(token)
    user_id = int(payload["sub"])
    user = db.query(models.User_table).filter(models.User_table.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    tenant = db.query(models.Tenant).filter(models.Tenant.id == user.tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=401, detail="Tenant not found")
    return tenant.schema_name


def get_schema_db(request: Request, db: Session = Depends(get_global_db), schema: str = Depends(get_current_schema)):
    db = sessionLocal()
    schema_regex = re.compile(r"^[a-z_][a-z0-9]{0,62}$")
    if not schema_regex.fullmatch(schema):
        raise HTTPException(status_code=401,detail="invalid schema")
    db.execute(text(f"SET SEARCH_PATH TO {schema},public"))
    try:
        yield db
    finally:
        db.close()

db_schema_dependency = Annotated[Session,Depends(get_schema_db)]

def create_token(data: dict):
    encode_data = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    encode_data.update({"exp":expire,"iat":datetime.now(timezone.utc),"nbf":datetime.now(timezone.utc)})
    if not access_key:
        raise Exception("secret key is not defined")
    if not algo:
        raise Exception("encrypting algorithm is not defined")
    access_token = jwt.encode(encode_data,access_key,algorithm=algo)
    return access_token
def create_refresh_token(data:dict):
    encode_data = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=3)
    encode_data.update({"exp":expire,"iat":datetime.now(timezone.utc),"nbf":datetime.now(timezone.utc)})
    if not refresh_key:
        raise Exception("secret key is not defined")
    if not algo:
        raise Exception("encrypting algorithm is not defined")
    refresh_token = jwt.encode(encode_data,refresh_key,algorithm=algo)
    return refresh_token

def get_org(user_id,db: Session):
    stmt = (
        select(models.User_table).where(models.User_table.user_id == user_id)
    )
    user = db.execute(stmt).scalars().first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user.tenant_id


class form_auth_data(BaseModel):
    Firstname: str
    Lastname: str
    Org_name: str
    Email_id: EmailStr
    Password: str
    class Config:
        json_schema_extra = {
            "example":{
                "org_name":"acme",
                "name": "john doe",
                "email_id":"johndoe@gmail.com",
                "password":"12344"
            }
        }

class form_data(BaseModel):
    email_id: str
    password: str
    org_name: str
    class Config:
        json_schema_extra = {
            "example":{
                "email_id": "johndoe@gmail.com",
                "password":"12344",
                "org_name":"acme",
            }
        }

class login_info(BaseModel):
    org_name: str
    email_id: EmailStr
    password: str
    class Config: 
        json_schema_extra = {
        "example": {
            "org_name": "acme",
            "email_id":"johndoe@gmail.com",
            "password": "12344"
            }
        }

@app.post("/logout/{session_id}",status_code=status.HTTP_200_OK)
def logout(session_id: int,db: db_dependency):
    user_session = db.query(models.User_session_table).filter(models.User_session_table.session_id == session_id).first()
    if user_session:
        user_session.revoked = True
        db.commit()
        return {"message":"Logged out successfully"}

@app.post("/signup/org",status_code=status.HTTP_201_CREATED)
def signup(form_auth_data: form_auth_data,db: db_dependency):
    tenant = db.query(models.Tenant).filter(models.Tenant.name == form_auth_data.Org_name).first()
    if tenant:
        raise HTTPException(status_code = 400,detail="Organisation already exists")
    else:
        try:
            schema_name = "tenant_"+form_auth_data.Org_name
            """ schema_regex = re.compile(r"^[a-z][a-z0-9_]{0,62}$")
            if not schema_regex.match(schema_name):
                raise HTTPException(status_code=400,detail="illegal schema name spotted") """
            new_tenant = models.Tenant(name=form_auth_data.Org_name,schema_name = "tenant_"+form_auth_data.Org_name)
            db.add(new_tenant)
            db.flush()
            hash_pwd = my_context.hash(form_auth_data.Password)
            admin_user = models.User_table(first_name=form_auth_data.Firstname,last_name=form_auth_data.Lastname,email_id = form_auth_data.Email_id,hashed_pwd=hash_pwd,role="Admin",is_active=True,tenant_id=new_tenant.id)
            db.add(admin_user)
            db.flush()
            db.execute(text(f"CREATE SCHEMA {schema_name}"))
            db.commit()
            migrate_tenant_schema(schema_name)
        except Exception as e:
            db.rollback()
            logger.exception("server error")
            raise HTTPException(status_code=500, detail=str(e.args))

    return {"tenant_id":new_tenant.id,"message":"Organisation successfully added"}
# function to return sessionid for auto login 
@app.post("/login",status_code=status.HTTP_200_OK)
def login_access(response: Response,form_data: form_data, db:db_dependency):
    try:
        tenant = db.query(models.Tenant).filter(models.Tenant.name == form_data.org_name).first()
        if not tenant:
            raise HTTPException(status_code=400,detail="organisation does not exist")
        user = db.query(models.User_table).filter(models.User_table.tenant_id == tenant.id and models.User_table.email_id == form_data.email_id).first()
        if not user:
            raise HTTPException(status_code=400,detail="user does not exist")
        if not my_context.verify(form_data.password,str(user.hashed_pwd)):
            raise HTTPException(status_code=401,detail="password is incorrect")
        new_session = models.User_session_table(user_id = user.user_id,refresh_token = None,expiry_date = datetime.now(timezone.utc) + timedelta(days=3),revoked=False)
        db.add(new_session)
        db.flush()
        refresh_token = create_refresh_token({"sub":str(user.user_id), "session_id": str(new_session.session_id)})
        hashed_refresh_token = hashlib.sha256(refresh_token.encode()).digest()
        new_session.refresh_token = hashed_refresh_token
        db.commit()
        db.refresh(new_session)
        login_access_token = create_token({"sub":str(user.user_id), "session_)id": str(new_session.session_id)})
        response.set_cookie (
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=24*60*60
        )
    except Exception as e:
        db.rollback()
        logger.exception("server error")
        raise HTTPException(status_code=500,detail="Server error")
    return {"access_token":login_access_token,"token_type":"Bearer"}

@app.post('/refresh',status_code=status.HTTP_200_OK)
def replenish_access(request: Request,db: db_dependency,response: Response):
    retrieved_refresh_token = request.cookies.get("refresh_token")
    if not retrieved_refresh_token:
        raise HTTPException(status_code=403,detail="access forbidden")
    hashed_token = hashed_refresh_token = hashlib.sha256(retrieved_refresh_token.encode()).digest()

    if not refresh_key:
        raise Exception("secret key is not defined")
    try:
        payload = jwt.decode(retrieved_refresh_token,refresh_key,algo)
        session_id = int(payload["session_id"])
        current_user_session = db.query(models.User_session_table).filter(models.User_session_table.session_id == session_id).first()
        if not current_user_session:
            return Response(status_code=404)
        if current_user_session.revoked == True:
            return Response(status_code=403)
        if current_user_session.refresh_token != hashed_refresh_token:
            return Response(status_code=404)
    except ExpiredSignatureError:
        return Response(status_code=401)
    except JWTError:
        return Response(status_code=403)
    try:
        new_refresh_token = create_refresh_token({"sub":str(payload["sub"]),"session_id":str(payload["session_id"])})
        hashed = hashlib.sha256(new_refresh_token.encode()).digest()
        current_user_session.refresh_token = hashed
        db.commit()
        db.refresh(current_user_session)
    except Exception:
        db.rollback()
        logger.exception("server error")
        raise HTTPException(status_code=500,detail="refresh failed")
    new_access_token = create_token({"sub":str(current_user_session.user_id), "session_id": current_user_session.session_id})
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=24*60*60
    )
    return {"access_token":new_access_token,"token_type":"Bearer"}
# document routes
@app.get("/documents/get",status_code=status.HTTP_200_OK)
def get_documents(db: db_schema_dependency,payload = Depends(JwtBearer)):
    user_id = payload["sub"]
    user = db.query(models.User_table).filter(models.User_table.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user_role = user.role
    org_id = get_org(user_id,db)
    stmt = (
        select(models.document_identity_table.id,models.document_permission_table.permissions).join(
            models.document_permission_table,
            models.document_identity_table.id == models.document_permission_table.document_id)
            .where(
                models.document_identity_table.permissions.any(user_role) | (models.document_permission_table.active & models.document_permission_table.permissions.any(user_id) )
            ).distinct()
    )
    docs = db.execute(stmt).all()
    response = []
    for doc,perm in docs:
        response.append({
            "id":doc.id,
            "permissions": perm
        })
    return response

#pending
""" @app.get("/documents/{id}",status_code=status.HTTP_200_OK)
def get_document(id: int, payload = Depends(JwtBearer)): """



