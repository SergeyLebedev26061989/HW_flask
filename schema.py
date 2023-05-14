import pydantic
from typing import Optional, Type, Union


class CreateAdver(pydantic.BaseModel):
    user: str
    title: str
    description: str
    # password: str

    # @pydantic.validator("password")
    # def validate_password(cls, value):
    #     if len(value) < 8:
    #         raise ValueError("Password is too short")
    #     return value


class PatchAdver(pydantic.BaseModel):
    user: Optional[str]
    title: Optional[str]
    description: Optional[str]

    # @pydantic.validator("password")
    # def validate_password(cls, value):
    #     if len(value) < 8:
    #         raise ValueError("Password is too short")
    #     return value


VALIDATION_CLASS = Union[Type[CreateAdver], Type[PatchAdver]]
