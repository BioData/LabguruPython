# labguru/resources/v2_reports.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class ReportsV2Resource(BaseResource):
    """API v2 reports: ``copy_section`` only. Use ``lab.reports`` for CRUD."""

    resource_name = "reports"
    api_version = "v2"
    item_key = "item"

    def copy_section(self, report_id, section_ids: list):
        """Copy sections (from experiments or protocols) into a report."""
        return self.client.post(
            self._path("/copy_section"),
            {self.item_key: {"item_id": report_id, "section_id": list(section_ids)}},
        )

    def list(self, *args, **kwargs):
        raise LabguruError("v2 reports supports copy_section only; use lab.reports")

    def get(self, *args, **kwargs):
        raise LabguruError("v2 reports supports copy_section only; use lab.reports")

    def create(self, *args, **kwargs):
        raise LabguruError("v2 reports supports copy_section only; use lab.reports")

    def update(self, *args, **kwargs):
        raise LabguruError("v2 reports supports copy_section only; use lab.reports")

    def delete(self, *args, **kwargs):
        raise LabguruError("v2 reports supports copy_section only; use lab.reports")
