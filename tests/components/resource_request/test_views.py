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

import pytest

from project.components.exceptions import NotFound
from project.components.resource_request.parameters import ResourceRequestSortByFields
from project.components.sorting import SortingOrder


class TestResourceRequestViews:
    async def test_list_resource_requests_returns_list_of_existing_resource_requests(
        self, client, jq, project_factory, resource_request_factory
    ):
        created_project = await project_factory.create()
        created_resource_request = await resource_request_factory.create(project_id=created_project.id)

        response = await client.get('/v1/resource-requests/')

        assert response.status_code == 200
        body = jq(response)
        received_resource_request_id = body('.result[].id').first()
        received_resource_request_project = body('.result[].project').first()
        received_total = body('.total').first()

        assert received_resource_request_id == str(created_resource_request.id)
        assert received_resource_request_project == {
            'name': created_resource_request.project.name,
            'code': created_resource_request.project.code,
        }
        assert received_total == 1

    async def test_get_resource_request_returns_resource_request_by_id(
        self, client, project_factory, resource_request_factory
    ):
        created_project = await project_factory.create()
        created_resource_request = await resource_request_factory.create(project_id=created_project.id)

        response = await client.get(f'/v1/resource-requests/{created_resource_request.id}')

        assert response.status_code == 200

        received_resource_request = response.json()

        assert received_resource_request['id'] == str(created_resource_request.id)
        assert received_resource_request['project'] == {
            'name': created_resource_request.project.name,
            'code': created_resource_request.project.code,
        }

    async def test_create_resource_request_creates_new_resource_request(
        self, client, jq, project_factory, resource_request_factory, resource_request_crud
    ):
        created_project = await project_factory.create()
        resource_request = resource_request_factory.generate(project_id=created_project.id)

        payload = resource_request.to_payload()
        response = await client.post('/v1/resource-requests/', json=payload)

        assert response.status_code == 200

        body = jq(response)
        received_resource_request_id = body('.id').first()
        received_resource_request = await resource_request_crud.retrieve_by_id(received_resource_request_id)

        assert received_resource_request.requested_for == resource_request.requested_for

    async def test_update_resource_request_updates_resource_request_field_by_id(
        self, client, jq, project_factory, resource_request_factory, resource_request_crud
    ):
        created_project = await project_factory.create()
        created_resource_request = await resource_request_factory.create(project_id=created_project.id)
        resource_request = resource_request_factory.generate()

        payload = {'user_id': resource_request.user_id}
        response = await client.patch(f'/v1/resource-requests/{created_resource_request.id}', json=payload)

        assert response.status_code == 200

        body = jq(response)
        received_resource_request_id = body('.id').first()
        received_resource_request = await resource_request_crud.retrieve_by_id(received_resource_request_id)

        assert received_resource_request.user_id == resource_request.user_id

    async def test_delete_resource_request(
        self, client, project_factory, resource_request_factory, resource_request_crud
    ):
        created_project = await project_factory.create()
        created_resource_request = await resource_request_factory.create(project_id=created_project.id)

        response = await client.delete(f'/v1/resource-requests/{created_resource_request.id}')

        assert response.status_code == 204

        with pytest.raises(NotFound):
            await resource_request_crud.retrieve_by_id(created_resource_request.id)

    @pytest.mark.parametrize('sort_by', ResourceRequestSortByFields.values())
    @pytest.mark.parametrize('sort_order', SortingOrder.values())
    async def test_list_resource_request_returns_results_sorted_by_field_with_proper_order(
        self, sort_by, sort_order, client, jq, project_factory, resource_request_factory
    ):
        created_project = await project_factory.create()
        created_resource_requests = await resource_request_factory.bulk_create(3, project_id=created_project.id)
        field_values = created_resource_requests.get_field_values(sort_by)
        if sort_by in ['requested_at', 'completed_at']:
            field_values = [key.isoformat() for key in field_values]
        if sort_by == 'project_id':
            field_values = [str(key) for key in field_values]
        expected_values = sorted(field_values, reverse=sort_order == SortingOrder.DESC)

        response = await client.get('/v1/resource-requests/', params={'sort_by': sort_by, 'sort_order': sort_order})

        body = jq(response)
        received_values = body(f'.result[].{sort_by}').all()
        received_total = body('.total').first()

        assert received_values == expected_values
        assert received_total == 3

    async def test_create_resource_request_returns_conflict_when_resource_from_same_user_to_same_project_exists(
        self, client, project_factory, resource_request_factory
    ):
        created_project = await project_factory.create()
        old_request_resource = await resource_request_factory.create(project_id=created_project.id)
        resource_request = resource_request_factory.generate(
            project_id=created_project.id,
            user_id=old_request_resource.user_id,
            requested_for=old_request_resource.requested_for,
        )

        payload = resource_request.to_payload()
        response = await client.post('/v1/resource-requests/', json=payload)

        assert response.status_code == 409
