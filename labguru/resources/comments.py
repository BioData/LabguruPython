# labguru/resources/comments.py
from labguru.resources.base import BaseResource


class CommentsResource(BaseResource):
    """Comments. list/get/create; the API has no update or delete endpoint."""

    resource_name = "comments"
    item_key = "item"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})
