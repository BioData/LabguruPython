# labguru/resources/experiments.py
from labguru.resources.base import BaseResource


class ExperimentsResource(BaseResource):
    resource_name = "experiments"
    item_key = "item"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})

    def elements(self, resource_id, element_type=None, name=None):
        """List an experiment's elements, optionally filtered by `element_type`
        (e.g. "text", "samples", "plate") and/or element `name`."""
        params = {k: v for k, v in (("element_type", element_type), ("name", name)) if v}
        return self.client.get(self._path(f"/{resource_id}/elements"), params=params or None)

    def set_flag(self, resource_id, flag_id):
        """Set the experiment's flag (POST /experiments/{id}/set_flag_as)."""
        return self.client.post(self._path(f"/{resource_id}/set_flag_as"), {"flag_id": flag_id})
