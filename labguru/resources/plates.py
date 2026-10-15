# labguru/resources/plates.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class PlatesResource(BaseResource):
    """Plates: list, get, delete, find_by_name and duplicate. Plates are created
    as plate elements (``elements.create``); the API has no POST/PUT on /plates."""

    resource_name = "plates"

    def find_by_name(self, name: str):
        return self.client.get(self._path("/find_by_name"), params={"name": name})

    def duplicate(self, resource_id, names: list):
        """Create one copy of the plate per name in `names`."""
        return self.client.post(self._path(f"/{resource_id}/duplicate"), {"names": names})

    def create(self, *args, **kwargs):
        raise LabguruError("plates has no create endpoint; add a plate element instead")

    def update(self, *args, **kwargs):
        raise LabguruError("plates has no update endpoint")
