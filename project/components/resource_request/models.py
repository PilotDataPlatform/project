from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from project.components.db_model import DBModel


class ResourceRequest(DBModel):
    """Resource Request Database Model."""

    __tablename__ = 'resource_requests'

    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False)
    requested_by_user_id = Column(String(length=256), nullable=False)
    requested_for = Column(String(length=256), nullable=False)
    requested_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
