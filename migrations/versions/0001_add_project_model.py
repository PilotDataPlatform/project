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
        sa.Column('code', sa.String(length=256), nullable=False),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.Column('description', sa.String(length=256), nullable=False),
        sa.Column('image_url', sa.String(length=2048), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('tags', postgresql.ARRAY(sa.String(length=256)), nullable=False),
        sa.Column('system_tags', postgresql.ARRAY(sa.String(length=256)), nullable=False),
        sa.Column('is_discoverable', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='project',
    )
    op.create_index(op.f('ix_project_projects_code'), 'projects', ['code'], unique=True, schema='project')


def downgrade():
    op.drop_index(op.f('ix_project_projects_code'), table_name='projects', schema='project')
    op.drop_table('projects', schema='project')
