from pydantic import BaseModel

class APIKeyRead(BaseModel):
    id: str
    key: str

    class Config:
        orm_mode = True
