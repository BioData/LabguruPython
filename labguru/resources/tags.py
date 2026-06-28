# labguru/resources/tags.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class TagsResource(BaseResource):
    """The Labguru tags API supports create (POST) and delete (DELETE) only —
    there is no list/show/update endpoint. ``delete(id)`` is inherited.
    """

    resource_name = "tags"
    item_key = "item"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})

    def list(self, *args, **kwargs):
        raise LabguruError("tags supports create and delete only; list is not available")

    def get(self, *args, **kwargs):
        raise LabguruError("tags supports create and delete only; get is not available")

    def update(self, *args, **kwargs):
        raise LabguruError("tags supports create and delete only; update is not available")
