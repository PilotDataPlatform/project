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

"""update resource_requests.

Revision ID: 0006
Revises: 0005
Create Date: 2022-07-06 10:41:50.362568
"""

import sqlalchemy as sa
from alembic import op

revision = '0006'
down_revision = '0005'
branch_labels = None
depends_on = '0005'


def upgrade():
    op.alter_column('resource_requests', 'requested_by_user_id', new_column_name='user_id', schema='project')
    op.add_column('resource_requests', sa.Column('username', sa.VARCHAR(length=256), nullable=False), schema='project')
    op.add_column('resource_requests', sa.Column('email', sa.VARCHAR(length=256), nullable=False), schema='project')
    op.create_index('user_id', 'resource_requests', ['project_id', 'requested_for'], unique=True, schema='project')


def downgrade():
    op.alter_column('resource_requests', 'user_id', new_column_name='requested_by_user_id', schema='project')
    op.drop_index('user_id', table_name='resource_requests', schema='project')
    op.drop_column('resource_requests', 'email', schema='project')
    op.drop_column('resource_requests', 'username', schema='project')
