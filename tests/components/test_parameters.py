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

import inspect

from project.components.pagination import Pagination
from project.components.parameters import PageParameters
from project.components.parameters import SortByFields
from project.components.parameters import SortParameters


class TestPageParameters:
    def test_to_pagination_returns_instance_of_pagination_with_the_same_page_arguments(self, fake):
        page = fake.pyint()
        page_size = fake.pyint()
        page_parameters = PageParameters(page=page, page_size=page_size)

        pagination = page_parameters.to_pagination()

        assert isinstance(pagination, Pagination)
        assert pagination.page == page
        assert pagination.page_size == page_size


class TestSortParameters:
    def test_with_sort_by_fields_returns_a_class_with_overridden_type_annotation_for_sort_by_field(self):
        class CustomSortByFields(SortByFields):
            field = 'field'

        sort_parameters_class = SortParameters.with_sort_by_fields(CustomSortByFields)

        signature = inspect.signature(sort_parameters_class)
        sort_by_field = signature.parameters['sort_by']

        assert sort_by_field.annotation is CustomSortByFields

    def test_with_sort_by_fields_does_not_override_original_class_type_annotation_for_sort_by_field(self):
        class CustomSortByFields(SortByFields):
            field = 'field'

        SortParameters.with_sort_by_fields(CustomSortByFields)

        signature = inspect.signature(SortParameters)
        sort_by_field = signature.parameters['sort_by']

        assert sort_by_field.annotation is str
