from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Base class for all available schemas."""


class ListResponseSchema(BaseSchema):
    """Default schema for multiple base schemas in response."""

    num_of_pages: int
    page: int
    total: int
    result: list[BaseSchema]
