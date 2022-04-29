import pytest

from project.components.exceptions import NotFound


class TestWorkbenchViews:
    async def test_list_workbenches_returns_list_of_existing_workbenches(
        self, client, project_factory, workbench_factory
    ):
        created_project = await project_factory.create()
        created_workbench = await workbench_factory.create(project_id=created_project.id)

        response = await client.get('/v1/workbenches/')

        assert response.status_code == 200

        body = response.json()
        received_workbench_id = body['result'][0]['id']
        received_total = body['total']

        assert received_workbench_id == str(created_workbench.id)
        assert received_total == 1

    async def test_get_workbench_returns_workbench_by_id(self, client, project_factory, workbench_factory):
        created_project = await project_factory.create()
        created_workbench = await workbench_factory.create(project_id=created_project.id)

        response = await client.get(f'/v1/workbenches/{created_workbench.id}')

        assert response.status_code == 200

        received_workbench = response.json()

        assert received_workbench['id'] == str(created_workbench.id)

    async def test_create_workbench_creates_new_workbench(
        self, client, project_factory, workbench_factory, workbench_crud
    ):
        created_project = await project_factory.create()
        workbench = workbench_factory.generate(project_id=created_project.id)

        payload = workbench.to_payload()
        response = await client.post('/v1/workbenches/', json=payload)

        assert response.status_code == 200

        body = response.json()
        received_workbench_id = body['id']
        received_workbench = await workbench_crud.retrieve_by_id(received_workbench_id)

        assert received_workbench.resource == workbench.resource

    async def test_update_workbench_updates_workbench_field_by_id(
        self, client, project_factory, workbench_factory, workbench_crud
    ):
        created_project = await project_factory.create()
        created_workbench = await workbench_factory.create(project_id=created_project.id)
        workbench = workbench_factory.generate()

        payload = {'deployed_by_user_id': workbench.deployed_by_user_id}
        response = await client.patch(f'/v1/workbenches/{created_workbench.id}', json=payload)

        assert response.status_code == 200

        body = response.json()
        received_workbench_id = body['id']
        received_workbench = await workbench_crud.retrieve_by_id(received_workbench_id)

        assert received_workbench.deployed_by_user_id == workbench.deployed_by_user_id

    async def test_delete_workbench(self, client, project_factory, workbench_factory, workbench_crud):
        created_project = await project_factory.create()
        created_workbench = await workbench_factory.create(project_id=created_project.id)

        response = await client.delete(f'/v1/workbenches/{created_workbench.id}')

        assert response.status_code == 204

        with pytest.raises(NotFound):
            await workbench_crud.retrieve_by_id(created_workbench.id)
