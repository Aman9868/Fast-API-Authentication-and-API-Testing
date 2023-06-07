from pydantic import BaseModel

class UserCreateSchema(BaseModel):
    email: str
    password: str

class UserLoginSchema(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
