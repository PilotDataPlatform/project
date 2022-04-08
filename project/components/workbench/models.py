from uuid import uuid4

from sqlalchemy import VARCHAR
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from project.components.db_model import DBModel


class Workbench(DBModel):
    """Workbench database model."""

    __tablename__ = 'workbenches'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False)
    resource = Column(VARCHAR(length=256), nullable=False)
    deployed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deployed_by_user_id = Column(VARCHAR(length=256), nullable=False)

    project = relationship('Project', back_populates='workbenches')
