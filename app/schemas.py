from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    id: int
    pass


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
