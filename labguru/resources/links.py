# labguru/resources/links.py
from labguru.resources.base import BaseResource


class LinksResource(BaseResource):
    """Links between items (source/target id+type or uuid): full CRUD."""

    resource_name = "links"
    item_key = "item"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})
