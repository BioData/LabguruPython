# labguru/resources/datasets.py
from labguru.resources.base import BaseResource


class DatasetsResource(BaseResource):
    """Datasets support list/get/create. The API has no update or delete
    endpoint (an inherited call to those raises LabguruAPIError(404)).
    """

    resource_name = "datasets"
    item_key = "item"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})
