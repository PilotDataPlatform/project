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

"""Add Project model.

Revision ID: 0001
Revises:
Create Date: 2022-04-04 18:58:48.883313
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'projects',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('code', sa.VARCHAR(length=32), nullable=False),
        sa.Column('name', sa.VARCHAR(length=256), nullable=False),
        sa.Column('description', sa.VARCHAR(length=256), nullable=False),
        sa.Column('image_url', sa.VARCHAR(length=2083), nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('tags', postgresql.ARRAY(sa.VARCHAR(length=256)), nullable=False),
        sa.Column('system_tags', postgresql.ARRAY(sa.VARCHAR(length=256)), nullable=False),
        sa.Column('is_discoverable', sa.BOOLEAN(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='project',
    )
    op.create_index(op.f('ix_project_projects_code'), 'projects', ['code'], unique=True, schema='project')


def downgrade():
    op.drop_index(op.f('ix_project_projects_code'), table_name='projects', schema='project')
    op.drop_table('projects', schema='project')
