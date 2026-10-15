# labguru/resources/storages.py
from labguru.resources.base import BaseResource


class StoragesResource(BaseResource):
    """Storages wrap writes under `system_storage_storage`, not `item` (per the API spec)."""

    resource_name = "storages"
    item_key = "system_storage_storage"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})
