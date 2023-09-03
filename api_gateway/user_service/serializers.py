import datetime

from pydantic import BaseModel, EmailStr, field_validator


class BaseUser(BaseModel):
    name: str
    surname: str
    username: str
    gender: int
    email: EmailStr

    @field_validator("name", "surname")
    def name_contain_space(cls, v):
        if " " in v:
            raise ValueError("Name or surname contain space")
        return v

    @field_validator("name", "surname")
    def name_contain_numeric(cls, v):
        if not v.isalpha:
            raise ValueError("Name or surname contains numbers")
        return v

    @field_validator("gender")
    def valid_gender(cls, v):
        if v not in [0, 1, 2]:
            raise ValueError("Gender is entered incorrectly")
        return v


class UserInDB(BaseUser):
    hashed_password: str


class UserIn(BaseUser):
    password: str


class UserOut(BaseUser):
    id: int
    created_at: datetime.datetime
    is_active: int
