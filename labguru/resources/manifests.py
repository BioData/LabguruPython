# labguru/resources/manifests.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class ManifestsResource(BaseResource):
    """Manifests: list and delete only."""

    resource_name = "manifests"

    def get(self, *args, **kwargs):
        raise LabguruError("manifests supports list and delete only; get is not available")

    def create(self, *args, **kwargs):
        raise LabguruError("manifests supports list and delete only; create is not available")

    def update(self, *args, **kwargs):
        raise LabguruError("manifests supports list and delete only; update is not available")
