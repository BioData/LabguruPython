# labguru/resources/documents.py
from labguru.resources.base import BaseResource


class DocumentsResource(BaseResource):
    """Documents. list/get/create/update; the API has no delete endpoint."""

    resource_name = "documents"
    item_key = "item"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})
