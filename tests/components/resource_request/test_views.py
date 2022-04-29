import pytest

from project.components.exceptions import NotFound


class TestResourceRequestViews:
    async def test_list_resource_requests_returns_list_of_existing_resource_requests(
        self, client, project_factory, resource_request_factory
    ):
        created_project = await project_factory.create()
        created_resource_request = await resource_request_factory.create(project_id=created_project.id)

        response = await client.get('/v1/resource-requests/')

        assert response.status_code == 200

        body = response.json()
        received_resource_request_id = body['result'][0]['id']
        received_total = body['total']

        assert received_resource_request_id == str(created_resource_request.id)
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

    async def test_create_resource_request_creates_new_resource_request(
        self, client, project_factory, resource_request_factory, resource_request_crud
    ):
        created_project = await project_factory.create()
        resource_request = resource_request_factory.generate(project_id=created_project.id)

        payload = resource_request.to_payload()
        response = await client.post('/v1/resource-requests/', json=payload)

        assert response.status_code == 200

        body = response.json()
        received_resource_request_id = body['id']
        received_resource_request = await resource_request_crud.retrieve_by_id(received_resource_request_id)

        assert received_resource_request.requested_for == resource_request.requested_for

    async def test_update_resource_request_updates_resource_request_field_by_id(
        self, client, project_factory, resource_request_factory, resource_request_crud
    ):
        created_project = await project_factory.create()
        created_resource_request = await resource_request_factory.create(project_id=created_project.id)
        resource_request = resource_request_factory.generate()

        payload = {'requested_by_user_id': resource_request.requested_by_user_id}
        response = await client.patch(f'/v1/resource-requests/{created_resource_request.id}', json=payload)

        assert response.status_code == 200

        body = response.json()
        received_resource_request_id = body['id']
        received_resource_request = await resource_request_crud.retrieve_by_id(received_resource_request_id)

        assert received_resource_request.requested_by_user_id == resource_request.requested_by_user_id

    async def test_delete_resource_request(
        self, client, project_factory, resource_request_factory, resource_request_crud
    ):
        created_project = await project_factory.create()
        created_resource_request = await resource_request_factory.create(project_id=created_project.id)

        response = await client.delete(f'/v1/resource-requests/{created_resource_request.id}')

        assert response.status_code == 204

        with pytest.raises(NotFound):
            await resource_request_crud.retrieve_by_id(created_resource_request.id)
