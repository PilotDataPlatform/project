from project.components.crud import CRUD
from project.components.workbench.models import Workbench


class WorkbenchCRUD(CRUD):
    """CRUD for managing workbench database models."""

    model = Workbench
