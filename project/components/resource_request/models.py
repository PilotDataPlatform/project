from datetime import datetime
from uuid import uuid4

from sqlalchemy import VARCHAR
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from project.components.db_model import DBModel


class ResourceRequest(DBModel):
    """Resource request database model."""

    __tablename__ = 'resource_requests'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False)
    requested_by_user_id = Column(VARCHAR(length=256), nullable=False)
    requested_for = Column(VARCHAR(length=256), nullable=False)
    requested_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    completed_at = Column(TIMESTAMP(timezone=True), nullable=True)

    project = relationship('Project', back_populates='resource_requests')
