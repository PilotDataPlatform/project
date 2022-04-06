"""Add Workbench model.

Revision ID: 0003
Revises: 0002
Create Date: 2022-04-05 19:27:02.257066
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = '0002'


def upgrade():
    op.create_table(
        'workbenches',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('resource', sa.String(length=256), nullable=False),
        sa.Column('deployed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deployed_by_user_id', sa.String(length=256), nullable=False),
        sa.ForeignKeyConstraint(
            ['project_id'],
            ['project.projects.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        schema='project',
    )


def downgrade():
    op.drop_table('workbenches', schema='project')
