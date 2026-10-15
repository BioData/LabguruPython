# labguru/resources/v2_experiments.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class ExperimentsV2Resource(BaseResource):
    """API v2 experiments: list and create. ``list`` accepts ``page``, ``page_size``,
    ``to_sign`` and ``to_witness``. ``create`` builds a full experiment in one call."""

    resource_name = "experiments"
    api_version = "v2"
    item_key = "item"

    def create(self, fields: dict):
        """fields: title, project_id, sections ([{title, elements: [...]}]) and
        milestone_id or milestone_name (an existing or new folder)."""
        return self.client.post(self._path(), {self.item_key: fields})

    def copy_section(self, experiment_id, section_ids: list):
        """Copy sections (from experiments or protocols) into an experiment."""
        return self.client.post(
            self._path("/copy_section"),
            {self.item_key: {"item_id": experiment_id, "section_id": list(section_ids)}},
        )

    def get(self, *args, **kwargs):
        raise LabguruError("v2 experiments supports list and create only; use lab.experiments.get")

    def update(self, *args, **kwargs):
        raise LabguruError("v2 experiments supports list and create only; use lab.experiments")

    def delete(self, *args, **kwargs):
        raise LabguruError("v2 experiments supports list and create only; use lab.experiments")
