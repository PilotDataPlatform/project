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

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from project.components.resource_request.crud import ResourceRequestCRUD
from project.dependencies import get_db_session


def get_resource_request_crud(db_session: AsyncSession = Depends(get_db_session)) -> ResourceRequestCRUD:
    """Return an instance of ResourceRequestCRUD as a dependency."""

    return ResourceRequestCRUD(db_session)
