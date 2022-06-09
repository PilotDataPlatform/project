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

"""Set Workbenches.deployed_at to UTC Now.

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
    op.alter_column('workbenches', 'deployed_at', nullable=False, schema='project')


def downgrade():
    op.alter_column('workbenches', 'deployed_at', nullable=True, schema='project')
