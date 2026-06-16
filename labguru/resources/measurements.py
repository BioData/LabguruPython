# labguru/resources/measurements.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class MeasurementsResource(BaseResource):
    """Create-only: POST /api/v1/measurements. The API has no list/get/update/delete
    endpoint. The body is ``{input_name, experiment_id, item}`` (not just ``item``).
    """

    resource_name = "measurements"

    def create(self, input_name: str, experiment_id, item: dict):
        """Record a measurement against an experiment input."""
        return self.client.post(
            self._path(),
            {"input_name": input_name, "experiment_id": experiment_id, "item": item},
        )

    def list(self, *args, **kwargs):
        raise LabguruError("measurements supports create only; list is not available")

    def get(self, *args, **kwargs):
        raise LabguruError("measurements supports create only; get is not available")

    def update(self, *args, **kwargs):
        raise LabguruError("measurements supports create only; update is not available")

    def delete(self, *args, **kwargs):
        raise LabguruError("measurements supports create only; delete is not available")
