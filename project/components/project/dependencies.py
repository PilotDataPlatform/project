from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from project.components.project.crud import ProjectCRUD
from project.dependencies import get_db_session


def get_project_crud(db_session: AsyncSession = Depends(get_db_session)) -> ProjectCRUD:
    """Return an instance of ProjectCRUD as a dependency."""

    return ProjectCRUD(db_session)
