import math

from pydantic import BaseModel
from pydantic import Field

from project.components import DBModel


class Pagination(BaseModel):
    """Pagination control parameters."""

    page: int = Field(default=0, ge=0)
    page_size: int = Field(default=20, ge=1)

    @property
    def limit(self) -> int:
        return self.page_size

    @property
    def offset(self) -> int:
        return self.page_size * self.page


class Page(BaseModel):
    """Represent one page of the response."""

    pagination: Pagination
    count: int
    entries: list[DBModel]

    class Config:
        arbitrary_types_allowed = True

    @property
    def number(self) -> int:
        return self.pagination.page

    @property
    def total_pages(self) -> int:
        return math.ceil(self.count / self.pagination.page_size)
