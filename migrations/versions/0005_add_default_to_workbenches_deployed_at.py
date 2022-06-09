"""Set Workbenches.deployed_at to UTC Now

Revision ID: 0005
Revises: 0004
Create Date: 2022-06-09 13:54:51.257512
"""

from alembic import op

revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = '0004'


def upgrade():
    op.execute("UPDATE project.workbenches SET deployed_at = (now() at time zone 'utc');")
    op.alter_column('workbenches', 'deployed_at',
        nullable=False,
        schema='project')


def downgrade():
    op.alter_column('workbenches', 'deployed_at',
        nullable=True,
        schema='project')
