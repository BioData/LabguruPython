# labguru/resources/visualizations.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class VisualizationsResource(BaseResource):
    """The Labguru visualizations API supports create (POST) and delete (DELETE)
    only — there is no list/show/update endpoint. ``delete(id)`` is inherited.
    """

    resource_name = "visualizations"
    item_key = "item"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})

    _READ_ONLY = "visualizations supports create and delete only"

    def list(self, *args, **kwargs):
        raise LabguruError(f"{self._READ_ONLY}; list is not available")

    def get(self, *args, **kwargs):
        raise LabguruError(f"{self._READ_ONLY}; get is not available")

    def update(self, *args, **kwargs):
        raise LabguruError(f"{self._READ_ONLY}; update is not available")
