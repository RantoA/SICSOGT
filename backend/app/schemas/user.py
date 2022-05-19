import typing as t

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    username: str = None
    im : int
    is_active: bool = True
    is_superuser: bool = False
    


# Properties to receive via API on creation
class UserCreate(UserBase):
    fonction_id: int = None
    

class UserOut(UserBase):
    id : int
    class Config:
        orm_mode = True

class UserEdit(UserBase):
    class Config:
        orm_mode = True

class UsermeEdit(BaseModel):
    username: str = None
    password: str
    class Config:
        orm_mode = True

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
