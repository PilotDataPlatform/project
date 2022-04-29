import pytest

from project.components.project.schemas import ProjectSchema


class TestProjectSchema:
    @pytest.mark.parametrize('code', ['0code', 'a', 'aa', 'a' * 33])
    def test_code_field_raises_value_error_for_invalid_values(self, code):
        with pytest.raises(ValueError):
            ProjectSchema(code=code, name='name')

    def test_code_field_strips_whitespaces(self):
        project = ProjectSchema(code=' code ', name='name')

        assert project.code == 'code'

    def test_name_field_strips_whitespaces(self):
        project = ProjectSchema(name=' name ', code='code')

        assert project.name == 'name'
