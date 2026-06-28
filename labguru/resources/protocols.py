# labguru/resources/protocols.py
from labguru.resources.base import BaseResource


class ProtocolsResource(BaseResource):
    resource_name = "protocols"
    item_key = "item"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post_form(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.put_form(self._path(f"/{resource_id}"), {self.item_key: fields})
