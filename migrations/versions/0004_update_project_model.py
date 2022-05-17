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

"""Update Project model.

Revision ID: 0004
Revises: 0003
Create Date: 2022-05-10 19:38:40.132501
"""

import sqlalchemy as sa
from alembic import op

revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = '0003'


def upgrade():
    op.alter_column(
        'projects',
        'description',
        type_=sa.VARCHAR(length=2048),
        schema='project',
    )
    op.alter_column(
        'projects',
        'image_url',
        new_column_name='logo_name',
        type_=sa.VARCHAR(length=40),
        schema='project',
    )


def downgrade():
    op.alter_column(
        'projects',
        'description',
        type_=sa.VARCHAR(length=256),
        schema='project',
    )
    op.alter_column(
        'projects',
        'logo_name',
        new_column_name='image_url',
        type_=sa.VARCHAR(length=2083),
        schema='project',
    )
