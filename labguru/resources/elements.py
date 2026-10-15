# labguru/resources/elements.py
import json

from labguru.resources.base import BaseResource


class ElementsResource(BaseResource):
    resource_name = "elements"
    item_key = "item"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        """fields: sent as the top-level body (the spec does not wrap element updates
        under `item`). Prefer `update_text` / `update_form`."""
        return self.client.put(self._path(f"/{resource_id}"), fields)

    def update_text(self, resource_id, data: str):
        """Replace a text element's content."""
        return self.update(resource_id, {"data": data})

    def update_form(self, resource_id, values: dict):
        """Update form-element fields; `values` maps field name -> new value and is
        sent as the `form_json` JSON string the API expects."""
        return self.update(resource_id, {"form_json": json.dumps(values)})

    def sort(self, container_id, ordered_ids, container_type="Projects::Experiment"):
        """Reorder elements in a container: `ordered_ids` is the full new order."""
        return self.client.post(
            self._path("/sort"),
            {"container_id": container_id, "container_type": container_type, "list": ordered_ids},
        )
