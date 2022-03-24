class TestResourceRequest:
    async def test_list_resource_requests(self, client):
        response = await client.get('/v1/resource-requests/')

        assert response.status_code == 501
        assert 'Not Implemented' in response.text

    async def test_get_resource_request(self, client, fake):
        resource_request_id = fake.uuid4()
        response = await client.get(f'/v1/resource-requests/{resource_request_id}')

        assert response.status_code == 501
        assert 'Not Implemented' in response.text

    async def test_create_resource_request(self, client):
        response = await client.post('/v1/resource-requests/', json={})

        assert response.status_code == 501
        assert 'Not Implemented' in response.text

    async def test_update_resource_request(self, client, fake):
        resource_request_id = fake.uuid4()
        response = await client.patch(f'/v1/resource-requests/{resource_request_id}', json={})

        assert response.status_code == 501
        assert 'Not Implemented' in response.text

    async def test_delete_resource_request(self, client, fake):
        resource_request_id = fake.uuid4()
        response = await client.delete(f'/v1/resource-requests/{resource_request_id}')

        assert response.status_code == 501
        assert 'Not Implemented' in response.text
