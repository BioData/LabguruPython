# labguru/resources/units.py
from labguru.resources.base import BaseResource


class UnitsResource(BaseResource):
    """Units. list/get/create/delete; the API has no update (PUT) endpoint."""

    resource_name = "units"
    item_key = "item"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})
