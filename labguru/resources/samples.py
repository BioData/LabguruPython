# labguru/resources/samples.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class SamplesResource(BaseResource):
    """Samples: delete, plus deleting a sample's instrument usage."""

    resource_name = "samples"

    def list(self, *args, **kwargs):
        raise LabguruError("samples supports delete only; list is not available")

    def get(self, *args, **kwargs):
        raise LabguruError("samples supports delete only; get is not available")

    def create(self, *args, **kwargs):
        raise LabguruError("samples supports delete only; create is not available")

    def update(self, *args, **kwargs):
        raise LabguruError("samples supports delete only; update is not available")

    def delete_instrument_usage(self, sample_id, usage_id):
        """DELETE /samples/{sample_id}/instrument_usages/{id}."""
        return self.client.delete(self._path(f"/{sample_id}/instrument_usages/{usage_id}"))
