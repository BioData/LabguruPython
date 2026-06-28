# labguru/resources/attachments.py
from labguru.resources.base import BaseResource


class AttachmentsResource(BaseResource):
    """Attachments are created via a multipart upload (POST /api/v1/attachments) and
    fetched/updated by id (GET/PUT /api/v1/attachments/{id}). The API has no list or
    delete endpoint.
    """

    resource_name = "attachments"
    item_key = "item"

    def create(self, files: dict, data: dict = None):
        """Upload an attachment via multipart/form-data.

        e.g. files={"item[attachment]": ("plate.csv", raw_bytes)},
             data={"item[title]": "plate.csv", "item[attachable_type]": "...",
                   "item[attach_to_uuid]": experiment_uuid}
        """
        return self.client.post_multipart(self._path(), files=files, data=data)

    def update(self, resource_id, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})
