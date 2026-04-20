from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv
from jose import jwt,JWTError
from sqlalchemy.orm import Session
from .main import db_dependency
from .models import models

load_dotenv()
key = os.getenv("SECRET_KEY")
algo = os.getenv("SECRET_ALGORITHM")

def decode_jwt(token):
    if not key:
        raise Exception("Secret key is not defined")
    payload = jwt.decode(token,key,algo)
    return payload

def get_current_user(db: db_dependency):
    async def jwt_bearer(request: Request) -> dict:
        bearer = HTTPBearer(auto_error=True)
        credentials: HTTPAuthorizationCredentials | None = await bearer(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=401,detail="Invalid authentication scheme")
            payload = verify_jwt(credentials.credentials, db)
            if payload is None:
                raise HTTPException(status_code=401,detail="Invalid or expired token")
            return payload
        else:
            raise HTTPException(status_code=401,detail="Invalid authorisation code")
    return jwt_bearer

def verify_jwt(token: str, db: Session) -> dict | None:
    try:
        payload = decode_jwt(token)
    except JWTError:
        return None
    session_id = payload.get("session_id")
    if not session_id:
        return None
    session = db.query(models.User_session_table).filter(models.User_session_table.session_id == session_id).first()
    if not session or session.revoked:
        return None
    return payload