from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from app.schemas.user import UserCreateSchema, UserLoginSchema, Token
from app.services.authentication import verify_password, get_password_hash, create_access_token, decode_access_token
from app.database.database import create_user, get_user_by_email, create_log,create_tables
from app.schemas.user import UserCreateSchema, UserLoginSchema, Token
from app.services import authentication
import logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = "125478"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION = timedelta(hours=24)

@app.get("/")
def home():
    return {"message": "Welcome to the API!"}

@app.post("/signup")
def sign_up(user: UserCreateSchema):
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    user_id = create_user(user.email, hashed_password)
    return {"user_id": user_id}

@app.post("/login")
def log_in(credentials: UserLoginSchema):
    user = get_user_by_email(credentials.email)
    if not user or not verify_password(credentials.password, user[2]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user[0])
    log_id = create_log(user[0], "login", "success")
    return Token(access_token=token, token_type="bearer")

def authenticate_user(token: HTTPAuthorizationCredentials = Depends(security)):
    user_id = decode_access_token(token.credentials)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user_id

@app.get("/protected")
def protected_route(user_id: int = Depends(authenticate_user)):
    log_id = create_log(user_id, "protected route", "success")
    return {"message": "This is a protected route"}

if __name__ == "__main__":
    create_tables()