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

from datetime import datetime
from datetime import timedelta
from itertools import islice

import pytest

from project.components.exceptions import NotFound
from project.components.project.parameters import ProjectSortByFields
from project.components.sorting import SortingOrder
from project.dependencies import get_s3_client


class TestProjectViews:
    async def test_list_projects_returns_list_of_existing_projects(self, client, jq, project_factory):
        created_project = await project_factory.create()

        response = await client.get('/v1/projects/')

        assert response.status_code == 200

        body = jq(response)
        received_project_id = body('.result[].id').first()
        received_total = body('.total').first()

        assert received_project_id == str(created_project.id)
        assert received_total == 1

    @pytest.mark.parametrize('sort_by', ProjectSortByFields.values())
    @pytest.mark.parametrize('sort_order', SortingOrder.values())
    async def test_list_projects_returns_results_sorted_by_field_with_proper_order(
        self, sort_by, sort_order, client, jq, project_factory
    ):
        created_projects = await project_factory.bulk_create(3)
        field_values = created_projects.get_field_values(sort_by)
        if sort_by == 'created_at':
            field_values = [key.isoformat() for key in field_values]
        expected_values = sorted(field_values, reverse=sort_order == SortingOrder.DESC)

        response = await client.get('/v1/projects/', params={'sort_by': sort_by, 'sort_order': sort_order})

        body = jq(response)
        received_values = body(f'.result[].{sort_by}').all()
        received_total = body('.total').first()

        assert received_values == expected_values
        assert received_total == 3

    @pytest.mark.parametrize('parameter', ['name', 'code', 'description'])
    async def test_list_projects_returns_project_filtered_by_parameter_full_match(
        self, parameter, client, jq, project_factory
    ):
        created_projects = await project_factory.bulk_create(3)
        project = created_projects.pop()

        response = await client.get('/v1/projects/', params={parameter: getattr(project, parameter)})

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert received_ids == [str(project.id)]
        assert received_total == 1

    async def test_list_projects_returns_projects_with_code_specified_in_code_any_parameter(
        self, client, jq, project_factory
    ):
        created_projects = await project_factory.bulk_create(3)
        mapping = created_projects.map_by_field('code')

        project_codes = [str(i) for i in islice(mapping.keys(), 2)]
        response = await client.get('/v1/projects/', params={'code_any': ','.join(project_codes)})

        body = jq(response)
        received_codes = body('.result[].code').all()
        received_total = body('.total').first()

        assert set(received_codes) == set(project_codes)
        assert received_total == 2

    async def test_list_projects_returns_projects_with_code_specified_in_code_any_parameter_even_if_only_one_matches(
        self, client, jq, fake, project_factory
    ):
        created_projects = await project_factory.bulk_create(2)
        project = created_projects.pop()

        project_codes = [fake.pystr(), fake.pystr(), project.code]
        response = await client.get('/v1/projects/', params={'code_any': ','.join(project_codes)})

        body = jq(response)
        received_codes = body('.result[].code').all()
        received_total = body('.total').first()

        assert received_codes == [project.code]
        assert received_total == 1

    async def test_list_projects_returns_project_with_tags_specified_in_tags_all_parameter(
        self, client, jq, project_factory
    ):
        created_projects = await project_factory.bulk_create(3)
        project = created_projects.pop()

        response = await client.get('/v1/projects/', params={'tags_all': ','.join(project.tags)})

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert received_ids == [str(project.id)]
        assert received_total == 1

    async def test_list_projects_returns_projects_with_tags_specified_in_tags_all_parameter_only_if_all_tags_match(
        self, client, jq, fake, project_factory
    ):
        tags = fake.words(3, unique=True)
        await project_factory.bulk_create(2, tags=tags[:-1])
        project = await project_factory.create(tags=tags)

        response = await client.get('/v1/projects/', params={'tags_all': ','.join(project.tags)})

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert received_ids == [str(project.id)]
        assert received_total == 1

    async def test_list_projects_returns_projects_filtered_by_created_at_start_and_created_at_end_parameters(
        self, client, jq, fake, project_factory
    ):
        today = datetime.now()
        week_ago = today - timedelta(days=7)
        two_weeks_ago = today - timedelta(days=14)

        [await project_factory.create(created_at=fake.date_between_dates(two_weeks_ago, week_ago)) for _ in range(2)]
        project = await project_factory.create(created_at=fake.date_time_between_dates(week_ago, today))

        params = {
            'created_at_start': int(datetime.timestamp(week_ago)),
            'created_at_end': int(datetime.timestamp(today)),
        }
        response = await client.get('/v1/projects/', params=params)

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert received_ids == [str(project.id)]
        assert received_total == 1

    @pytest.mark.parametrize('is_discoverable', [True, False])
    async def test_list_projects_returns_projects_filtered_by_value_in_is_discoverable_parameter(
        self, is_discoverable, client, jq, project_factory
    ):
        await project_factory.bulk_create(2, is_discoverable=not is_discoverable)
        created_projects = await project_factory.bulk_create(2, is_discoverable=is_discoverable)
        mapping = created_projects.map_by_field('id', str)
        expected_ids = list(mapping.keys())

        response = await client.get('/v1/projects/', params={'is_discoverable': str(is_discoverable).lower()})

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert set(received_ids) == set(expected_ids)
        assert received_total == 2

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

    async def test_create_project_creates_new_project(self, client, jq, project_factory, project_crud):
        project = project_factory.generate()

        payload = project.to_payload()
        response = await client.post('/v1/projects/', json=payload)

        assert response.status_code == 200

        body = jq(response)
        received_project_id = body('.id').first()
        received_project = await project_crud.retrieve_by_id(received_project_id)

        assert received_project.code == project.code

    async def test_create_project_returns_conflict_response_when_project_with_same_code_already_exists(
        self, client, project_factory, project_crud
    ):
        created_project = await project_factory.create()
        project = project_factory.generate(code=created_project.code)

        payload = project.to_payload()
        response = await client.post('/v1/projects/', json=payload)

        assert response.status_code == 409

    async def test_update_project_updates_project_field_by_id(self, client, jq, project_factory, project_crud):
        created_project = await project_factory.create()
        project = project_factory.generate()

        payload = {'description': project.description}
        response = await client.patch(f'/v1/projects/{created_project.id}', json=payload)

        assert response.status_code == 200

        body = jq(response)
        received_project_id = body('.id').first()
        received_project = await project_crud.retrieve_by_id(received_project_id)

        assert received_project.description == project.description

    async def test_delete_project_removes_project_by_id(self, client, project_factory, project_crud):
        created_project = await project_factory.create()

        response = await client.delete(f'/v1/projects/{created_project.id}')

        assert response.status_code == 204

        with pytest.raises(NotFound):
            await project_crud.retrieve_by_id(created_project.id)

    async def test_upload_project_logo_calls_put_object_method_and_updates_project_logo_name(
        self, client, jq, override_dependencies, s3_client, project_factory, fake, project_crud
    ):
        created_project = await project_factory.create()
        expected_logo_name = f'{created_project.id}.png'

        payload = {'base64': fake.base64_image()}

        with override_dependencies({get_s3_client: lambda: s3_client}):
            response = await client.post(f'/v1/projects/{created_project.id}/logo', json=payload)

        assert response.status_code == 200

        s3_client.put_object.assert_called_once()

        body = jq(response)
        received_project_id = body('.id').first()
        received_project = await project_crud.retrieve_by_id(received_project_id)

        assert received_project.logo_name == expected_logo_name

    async def test_upload_project_logo_returns_not_found_response_for_non_existing_project(self, client, fake):
        project_id = fake.uuid4()
        payload = {'base64': fake.base64_image()}

        response = await client.post(f'/v1/projects/{project_id}/logo', json=payload)

        assert response.status_code == 404
