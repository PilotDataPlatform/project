class TestProjectViews:
    async def test_list_projects1(self, client):
        response = await client.get('/v1/projects/')

        assert response.status_code == 501
        assert 'Not Implemented' in response.text

    async def test_get_project(self, client, fake):
        project_id = fake.uuid4()
        response = await client.get(f'/v1/projects/{project_id}')

        assert response.status_code == 501
        assert 'Not Implemented' in response.text

    async def test_create_project(self, client):
        response = await client.post('/v1/projects/', json={})

        assert response.status_code == 501
        assert 'Not Implemented' in response.text

    async def test_update_project(self, client, fake):
        project_id = fake.uuid4()
        response = await client.patch(f'/v1/projects/{project_id}', json={})

        assert response.status_code == 501
        assert 'Not Implemented' in response.text

    async def test_delete_project(self, client, fake):
        project_id = fake.uuid4()
        response = await client.delete(f'/v1/projects/{project_id}')

        assert response.status_code == 501
        assert 'Not Implemented' in response.text
