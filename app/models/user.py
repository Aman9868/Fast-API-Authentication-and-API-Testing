from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str

class UserCreate(BaseModel):
    email: str
    password: str
