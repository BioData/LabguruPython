# labguru/resources/reports.py
from labguru.resources.base import BaseResource


class ReportsResource(BaseResource):
    """Reports. list/get/create/update; the API has no delete endpoint. The API also
    exposes POST /api/v1/reports/add_cover_to_report and .../add_section_to_report,
    not modeled here.
    """

    resource_name = "reports"
    item_key = "item"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})

    def add_section(self, report_id, section_id):
        """Copy an existing section into a report."""
        return self.client.post(
            self._path("/add_section_to_report"),
            {self.item_key: {"report_id": report_id, "section_id": str(section_id)}},
        )

    def add_cover(self, report_id, data: str):
        """Set the report's cover page content (`data`)."""
        return self.client.post(
            self._path("/add_cover_to_report"),
            {self.item_key: {"report_id": report_id, "data": data}},
        )
