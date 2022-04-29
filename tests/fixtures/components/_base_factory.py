from faker import Faker

from project.components.crud import CRUD


class BaseFactory:
    """Base class for creating testing purpose entries."""

    crud: CRUD
    fake: Faker

    def __init__(self, crud: CRUD, fake: Faker) -> None:
        self.crud = crud
        self.fake = fake
