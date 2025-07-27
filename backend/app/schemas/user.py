from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

class UserRead(BaseModel):
    id: str
    email: EmailStr
    full_name: str | None = None

    class Config:
        orm_mode = True
