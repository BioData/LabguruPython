# labguru/resources/v2_compound_parent_structures.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class CompoundParentStructuresV2Resource(BaseResource):
    """API v2 compound parent structures: list, get, update and their compounds.
    Updates wrap under ``parent_structure`` (not ``item``)."""

    resource_name = "compound_parent_structures"
    api_version = "v2"
    item_key = "parent_structure"

    def update(self, resource_id, fields: dict):
        """fields: owner_id and/or name."""
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})

    def compounds(self, resource_id):
        """Compounds that share this parent structure."""
        return self.client.get(self._path(f"/{resource_id}/compounds"))

    def create(self, *args, **kwargs):
        raise LabguruError("compound_parent_structures has no create endpoint")

    def delete(self, *args, **kwargs):
        raise LabguruError("compound_parent_structures has no delete endpoint")
