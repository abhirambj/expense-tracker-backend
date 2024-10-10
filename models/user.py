from typing import Optional

from pydantic import BaseModel, EmailStr
from uuid import UUID


class User(BaseModel):
    id: Optional[UUID] = None
    username: str
    email: EmailStr


class CreateUser(User):
    password: str
    confirm_password: str


class UserLogin(BaseModel):
    username: str
    password: str
