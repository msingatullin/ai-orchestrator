from __future__ import annotations

from pydantic import BaseModel

class BaseSettings(BaseModel):
    def model_dump(self) -> dict:
        return self.__dict__
