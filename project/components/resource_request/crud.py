from project.components.crud import CRUD
from project.components.resource_request.models import ResourceRequest


class ResourceRequestCRUD(CRUD):
    """CRUD for managing resource request database models."""

    model = ResourceRequest
