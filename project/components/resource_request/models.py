# Copyright (C) 2022 Indoc Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from uuid import uuid4

from sqlalchemy import VARCHAR
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from project.components.db_model import DBModel


class ResourceRequest(DBModel):
    """Resource request database model."""

    __tablename__ = 'resource_requests'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False)
    user_id = Column(VARCHAR(length=256), nullable=False)
    username = Column(VARCHAR(length=256), nullable=False)
    email = Column(VARCHAR(length=256), nullable=False)
    requested_for = Column(VARCHAR(length=256), nullable=False)
    requested_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    completed_at = Column(TIMESTAMP(timezone=True), nullable=True)

    project = relationship('Project', back_populates='resource_requests')

    __table_args__ = (
        Index(
            'user_id',
            'project_id',
            'requested_for',
            unique=True,
        ),
        {'schema': 'project'},
    )
