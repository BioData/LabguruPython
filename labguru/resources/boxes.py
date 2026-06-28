# labguru/resources/boxes.py
from labguru.resources.base import BaseResource


class BoxesResource(BaseResource):
    """Storage boxes. list/get/create/update; the API has no delete endpoint."""

    resource_name = "boxes"
    item_key = "item"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})
