from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str