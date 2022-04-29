from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from project.components.workbench.crud import WorkbenchCRUD
from project.dependencies import get_db_session


def get_workbench_crud(db_session: AsyncSession = Depends(get_db_session)) -> WorkbenchCRUD:
    """Return an instance of WorkbenchCRUD as a dependency."""

    return WorkbenchCRUD(db_session)
