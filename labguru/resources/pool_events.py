# labguru/resources/pool_events.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class PoolEventsResource(BaseResource):
    """Sample pooling events: create only. ``pool_type`` in the body selects the
    fixed / custom / consume variant (see the spec)."""

    resource_name = "pool_events"
    item_key = "item"

    def create(self, fields: dict):
        """fields: name, pool_type, unit, unit_type, pooled_stock_info and either
        stocks_list (fixed: + fixed_amount; consume) or stocks_usage (custom)."""
        return self.client.post(self._path(), {self.item_key: fields})

    def list(self, *args, **kwargs):
        raise LabguruError("pool_events supports create only; list is not available")

    def get(self, *args, **kwargs):
        raise LabguruError("pool_events supports create only; get is not available")

    def update(self, *args, **kwargs):
        raise LabguruError("pool_events supports create only; update is not available")

    def delete(self, *args, **kwargs):
        raise LabguruError("pool_events supports create only; delete is not available")
