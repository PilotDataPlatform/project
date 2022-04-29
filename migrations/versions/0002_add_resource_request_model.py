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

"""Add Resource Request model.

Revision ID: 0002
Revises: 0001
Create Date: 2022-04-05 15:50:47.603266
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = '0001'


def upgrade():
    op.create_table(
        'resource_requests',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('requested_by_user_id', sa.VARCHAR(length=256), nullable=False),
        sa.Column('requested_for', sa.VARCHAR(length=256), nullable=False),
        sa.Column('requested_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('completed_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ['project_id'],
            ['project.projects.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        schema='project',
    )


def downgrade():
    op.drop_table('resource_requests', schema='project')
