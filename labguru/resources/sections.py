# labguru/resources/sections.py
from labguru.resources.base import BaseResource


class SectionsResource(BaseResource):
    resource_name = "sections"
    item_key = "item"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})

    def sort(self, container_id, ordered_ids, container_type="Projects::Experiment"):
        """Reorder sections in a container: `ordered_ids` is the full new order."""
        return self.client.post(
            self._path("/sort"),
            {"container_id": container_id, "container_type": container_type, "list": ordered_ids},
        )
