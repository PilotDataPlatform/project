class TestWorkbench:
    async def test_list_workbenches(self, client):
        response = await client.get('/v1/workbenches/')

        assert response.status_code == 501
        assert 'Not Implemented' in response.text

    async def test_get_workbench(self, client, fake):
        workbench_id = fake.uuid4()
        response = await client.get(f'/v1/workbenches/{workbench_id}')

        assert response.status_code == 501
        assert 'Not Implemented' in response.text

    async def test_create_workbench(self, client):
        response = await client.post('/v1/workbenches/', json={})

        assert response.status_code == 501
        assert 'Not Implemented' in response.text

    async def test_update_workbench(self, client, fake):
        workbench_id = fake.uuid4()
        response = await client.patch(f'/v1/workbenches/{workbench_id}', json={})

        assert response.status_code == 501
        assert 'Not Implemented' in response.text

    async def test_delete_workbench(self, client, fake):
        workbench_id = fake.uuid4()
        response = await client.delete(f'/v1/workbenches/{workbench_id}')

        assert response.status_code == 501
        assert 'Not Implemented' in response.text
