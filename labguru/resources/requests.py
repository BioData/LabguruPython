# labguru/resources/requests.py
from labguru.resources.base import BaseResource


class RequestsResource(BaseResource):
    """Requests. list/get/create/update; the API has no delete endpoint. State
    transitions (accept/approve/done/reject/select_performer/start/submit) are
    PATCH /api/v1/requests/{id}/<action> and are not modeled here.
    """

    resource_name = "requests"
    item_key = "item"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})
