from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv
from jose import jwt,JWTError

load_dotenv()
key = os.getenv("SECRET_KEY")
algo = os.getenv("SECRET_ALGORITHM")
def decode_jwt(token):
    if not key:
        raise Exception("Secret key is not defined")
    payload = jwt.decode(token,key,algo)
    return payload

class JwtBearer(HTTPBearer):
    def __init__(self,auto_error: bool = True):
        super().__init__(auto_error=auto_error)
    async def __call__(self,request:Request):
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=401,detail="Invalid authentication scheme")
            payload = self.verify_jwt(credentials.credentials)
            if payload is None:
                raise HTTPException(status_code=401,detail="Invalid or expired token")
            return payload
        else:
            raise HTTPException(status_code=401,detail="Invalid authorisation code")
    
    def verify_jwt(self,token):
        try:
            payload = decode_jwt(token)
        except JWTError:
            return None
        return payload