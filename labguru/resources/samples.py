# labguru/resources/samples.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class SamplesResource(BaseResource):
    """Samples: the links between inventory items and a samples/equipment element.
    create (POST /samples; not in the published spec, but used live by
    labguru-api-examples#4), delete, and deleting a sample's instrument usage."""

    resource_name = "samples"
    item_key = "item"

    def create(self, fields: dict):
        """fields: container_type, container_id, item_id, item_type — wrapped under `item`."""
        return self.client.post(self._path(), {self.item_key: fields})

    def link(self, element_id, item_id, item_type: str):
        """Link an inventory item (e.g. item_type "Catalog::Material" or
        "System::Instrument") to a samples/equipment element."""
        return self.create({
            "container_type": "Element", "container_id": element_id,
            "item_id": item_id, "item_type": item_type,
        })

    def list(self, *args, **kwargs):
        raise LabguruError("samples supports create and delete only; list is not available")

    def get(self, *args, **kwargs):
        raise LabguruError("samples supports create and delete only; get is not available")

    def update(self, *args, **kwargs):
        raise LabguruError("samples supports create and delete only; update is not available")

    def delete_instrument_usage(self, sample_id, usage_id):
        """DELETE /samples/{sample_id}/instrument_usages/{id}."""
        return self.client.delete(self._path(f"/{sample_id}/instrument_usages/{usage_id}"))
