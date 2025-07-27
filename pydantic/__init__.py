from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional


def Field(default: Any = None, default_factory: Optional[Callable[[], Any]] = None, alias: str | None = None):
    if default_factory is not None:
        return default_factory()
    return default


class BaseModel:
    def __init__(self, **data: Any):
        for k, v in data.items():
            setattr(self, k, v)

    def model_dump(self) -> dict:
        return self.__dict__


class ValidationError(Exception):
    pass


# minimal submodule for config compatibility
class config:
    ConfigDict = dict


__all__ = ["BaseModel", "Field", "ValidationError", "config"]
