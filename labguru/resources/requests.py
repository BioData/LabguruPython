# labguru/resources/requests.py
from labguru.resources.base import BaseResource


class RequestsResource(BaseResource):
    """Requests: CRUD plus the workflow transitions
    (submit/approve/accept/select_performer/start/done/reject), each a
    PATCH /api/v1/requests/{id}/<action>.
    """

    resource_name = "requests"
    item_key = "item"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})

    def _transition(self, resource_id, action: str, fields=None):
        body = {self.item_key: fields} if fields else None
        return self.client.patch(self._path(f"/{resource_id}/{action}"), body)

    def submit(self, resource_id, **fields):
        """fields: optional name, team_id, due_date."""
        return self._transition(resource_id, "submit", fields)

    def approve(self, resource_id, **fields):
        """fields: optional team_id, due_date, priority."""
        return self._transition(resource_id, "approve", fields)

    def accept(self, resource_id, **fields):
        """fields: optional priority."""
        return self._transition(resource_id, "accept", fields)

    def select_performer(self, resource_id, performed_by):
        return self._transition(resource_id, "select_performer", {"performed_by": performed_by})

    def start(self, resource_id, **fields):
        """fields: optional performed_by."""
        return self._transition(resource_id, "start", fields)

    def done(self, resource_id):
        return self._transition(resource_id, "done")

    def reject(self, resource_id):
        return self._transition(resource_id, "reject")
