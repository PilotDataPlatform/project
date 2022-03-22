from uuid import uuid4

from components.db_model import DBModel
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID


class Workbench(DBModel):
    """Workbench Database Model."""

    __tablename__ = 'workbenches'

    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False)
    resource = Column(String(length=256), nullable=False)
    deployed_at = Column(DateTime(timezone=True), nullable=True)
    deployed_by_user_id = Column(String(length=256), nullable=False)
