# labguru/resources/storages.py
from labguru.resources.base import BaseResource


class StoragesResource(BaseResource):
    resource_name = "storages"
    item_key = "item"

    def create(self, fields: dict):
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})

    def boxes(self, resource_id):
        """GET the storage's boxes."""
        return self.client.get(self._path(f"/{resource_id}/boxes"))
