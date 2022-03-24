from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from project.components.db_model import DBModel


class Project(DBModel):
    """Project Database Model."""

    __tablename__ = 'projects'

    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    code = Column(String(length=256), unique=True, index=True, nullable=False)
    name = Column(String(length=256), nullable=False)
    description = Column(String(length=256), nullable=False)
    image_url = Column(String(length=2048), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow, nullable=False)
    tags = Column(ARRAY(String(256)), nullable=False)
    system_tags = Column(ARRAY(String(256)), nullable=False)
    is_discoverable = Column(Boolean(), default=True, nullable=False)

    resource_requests = relationship('ResourceRequest', uselist=True, cascade='all, delete-orphan', backref='projects')
