import pytest

from project.components.exceptions import NotFound


class TestProjectViews:
    async def test_list_projects_returns_list_of_existing_projects(self, client, project_factory):
        created_project = await project_factory.create()

        response = await client.get('/v1/projects/')

        assert response.status_code == 200

        body = response.json()
        received_project_id = body['result'][0]['id']
        received_total = body['total']

        assert received_project_id == str(created_project.id)
        assert received_total == 1

    async def test_get_project_returns_project_by_id(self, client, project_factory):
        created_project = await project_factory.create()

        response = await client.get(f'/v1/projects/{created_project.id}')

        assert response.status_code == 200

        received_project = response.json()

        assert received_project['id'] == str(created_project.id)

    async def test_get_project_returns_project_by_code(self, client, project_factory):
        created_project = await project_factory.create()

        response = await client.get(f'/v1/projects/{created_project.code}')

        assert response.status_code == 200

        received_project = response.json()

        assert received_project['id'] == str(created_project.id)

    async def test_create_project_creates_new_project(self, client, project_factory, project_crud):
        project = project_factory.generate()

        payload = project.to_payload()
        response = await client.post('/v1/projects/', json=payload)

        assert response.status_code == 200

        body = response.json()
        received_project_id = body['id']
        received_project = await project_crud.retrieve_by_id(received_project_id)

        assert received_project.code == project.code

    async def test_update_project_updates_project_field_by_id(self, client, project_factory, project_crud):
        created_project = await project_factory.create()
        project = project_factory.generate()

        payload = {'description': project.description}
        response = await client.patch(f'/v1/projects/{created_project.id}', json=payload)

        assert response.status_code == 200

        body = response.json()
        received_project_id = body['id']
        received_project = await project_crud.retrieve_by_id(received_project_id)

        assert received_project.description == project.description

    async def test_delete_project(self, client, project_factory, project_crud):
        created_project = await project_factory.create()

        response = await client.delete(f'/v1/projects/{created_project.id}')

        assert response.status_code == 204

        with pytest.raises(NotFound):
            await project_crud.retrieve_by_id(created_project.id)
