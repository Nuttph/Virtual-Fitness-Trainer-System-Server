from pydantic import BaseModel,EmailStr
from datetime import date

class UserRegister(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    img:str | None = None
    birthdate: date
    weight: float
    height: float
    gender: int

class UserEdit(BaseModel):
    password:str
    firstname:str
    lastname:str
    brithdate:date
    weight: float
    height: float
    gender: int

