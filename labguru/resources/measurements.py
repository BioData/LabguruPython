# labguru/resources/measurements.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class MeasurementsResource(BaseResource):
    """Create and delete: POST /api/v1/measurements, DELETE /api/v1/measurements/{id}.
    The API has no list/get/update endpoint. The body is
    ``{input_name, experiment_id, item}`` (not just ``item``).
    """

    resource_name = "measurements"

    def create(self, input_name: str, experiment_id, item: dict):
        """Record a measurement against an experiment input."""
        return self.client.post(
            self._path(),
            {"input_name": input_name, "experiment_id": experiment_id, "item": item},
        )

    def list(self, *args, **kwargs):
        raise LabguruError("measurements supports create and delete only; list is not available")

    def get(self, *args, **kwargs):
        raise LabguruError("measurements supports create and delete only; get is not available")

    def update(self, *args, **kwargs):
        raise LabguruError("measurements supports create and delete only; update is not available")
