from fastapi import Query
from pydantic import BaseModel

from project.components.pagination import Pagination


class PageParameters(BaseModel):
    """Query parameters for pagination."""

    page: int = Query(default=0, ge=0)
    page_size: int = Query(default=20, ge=1)

    def to_pagination(self) -> Pagination:
        return Pagination(page=self.page, page_size=self.page_size)
