# labguru/resources/stocks.py
from labguru.resources.base import BaseResource


class StocksResource(BaseResource):
    resource_name = "stocks"
    item_key = "item"

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})

    def mark_as_consumed(self, resource_id):
        return self.client.post(self._path(f"/{resource_id}/mark_as_consumed"))

    def mark_as_output(self, resource_id, experiment_id):
        """Mark the stock as an output of an experiment."""
        return self.client.post(
            self._path(f"/{resource_id}/mark_as_output"), {"exp_id": experiment_id}
        )

    def unmark_output(self, resource_id, experiment_id):
        return self.client.post(
            self._path(f"/{resource_id}/unmark_output"), {"exp_id": experiment_id}
        )

    def update_stock_amount(
        self, resource_id, amount_used, unit_type_name, unit_type=None,
        subtract=True, element_id=None, sample_id=None,
    ):
        """Record usage against a stock (typically from a samples element).

        unit_type: "weight" or "volume"; unit_type_name: e.g. "mg", "mL".
        """
        body = {
            "amount_used": str(amount_used),
            "unit_type_name": unit_type_name,
            "subtract": "true" if subtract else "false",
        }
        optional = (("unit_type", unit_type), ("element_id", element_id), ("sample_id", sample_id))
        body.update({k: v for k, v in optional if v is not None})
        return self.client.post(self._path(f"/{resource_id}/update_stock_amount"), body)

    def find_by_barcode(self, barcode: str):
        """GET /stocks/get_stocks_by_barcode?input=<barcode>."""
        return self.client.get(self._path("/get_stocks_by_barcode"), params={"input": barcode})
