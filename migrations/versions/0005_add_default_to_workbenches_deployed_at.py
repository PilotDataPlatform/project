"""add_default_to_workbenches_deployed_at

Revision ID: 0005
Revises: 0004
Create Date: 2022-06-09 13:54:51.257512
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = '0004'


def upgrade():
    op.execute("UPDATE project.workbenches SET deployed_at = now();")
    op.alter_column('workbenches', 'deployed_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("(now() at time zone 'utc')"),
        nullable=False,
        schema='project')


def downgrade():
    op.alter_column('workbenches', 'deployed_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        nullable=True,
        schema='project')
