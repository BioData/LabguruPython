# labguru/resources/projects.py
from labguru.resources.base import BaseResource


class ProjectsResource(BaseResource):
    resource_name = "projects"
    item_key = "item"

    def create(self, fields: dict):
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})
