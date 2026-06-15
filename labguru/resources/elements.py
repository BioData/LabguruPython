# labguru/resources/elements.py
from labguru.resources.base import BaseResource


class ElementsResource(BaseResource):
    resource_name = "elements"
    item_key = "item"

    def create(self, fields: dict):
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})
