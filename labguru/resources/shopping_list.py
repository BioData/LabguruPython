# labguru/resources/shopping_list.py
from labguru.resources.base import BaseResource


class ShoppingListResource(BaseResource):
    """Shopping list: list, get, update, delete, plus add_item and the
    submit/approve/cancel transitions. Items are added with ``add_item``
    (``POST /shopping_list/add_item``); there is no plain POST /shopping_list."""

    resource_name = "shopping_list"
    item_key = "item"

    def add_item(self, fields: dict):
        """fields: collection_type, item_id, quantity (+ collection_id for custom
        collections; optional price, currency, remarks), wrapped under `item`."""
        return self.client.post(self._path("/add_item"), {self.item_key: fields})

    def create(self, fields: dict):
        """Alias for `add_item` (the API's only create endpoint)."""
        return self.add_item(fields)

    def update(self, resource_id, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})

    def submit(self, resource_id):
        return self.client.put(self._path(f"/{resource_id}/submit"))

    def approve(self, resource_id):
        return self.client.put(self._path(f"/{resource_id}/approve"))

    def cancel(self, resource_id):
        return self.client.put(self._path(f"/{resource_id}/cancel"))
