# labguru/resources/elements.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class ElementsResource(BaseResource):
    resource_name = "elements"
    item_key = "item"

    def list(self, *args, **kwargs):
        raise LabguruError("elements has no list endpoint in the API; use experiments.elements(id)")

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})
