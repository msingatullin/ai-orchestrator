from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    organization_id: str | None = None
    role: str | None = None

class UserRead(BaseModel):
    id: str
    email: EmailStr
    full_name: str | None = None
    organization_id: str | None = None
    role: str

    class Config:
        orm_mode = True
