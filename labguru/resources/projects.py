# labguru/resources/projects.py
from labguru.resources.base import BaseResource


class ProjectsResource(BaseResource):
    resource_name = "projects"
    item_key = "item"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})

    def delete(self, resource_id):
        """Project delete exists only in API v2: DELETE /api/v2/projects/{id}."""
        return self.client.delete(f"/api/v2/{self.resource_name}/{resource_id}")
