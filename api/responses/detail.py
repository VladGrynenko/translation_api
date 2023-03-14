from pydantic import BaseModel


class DetailResponse(BaseModel):
    message: dict


class StringResponse(BaseModel):
    message: str


class ListResponse(BaseModel):
    message: list
