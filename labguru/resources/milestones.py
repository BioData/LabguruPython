# labguru/resources/milestones.py
from labguru.resources.base import BaseResource


class MilestonesResource(BaseResource):
    """Folders (`/api/v1/milestones`, the 1.x Folder) within a project: full CRUD."""

    resource_name = "milestones"
    item_key = "item"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})
