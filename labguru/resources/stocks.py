# labguru/resources/stocks.py
from labguru.resources.base import BaseResource


class StocksResource(BaseResource):
    resource_name = "stocks"
    item_key = "item"

    def create(self, fields: dict):
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})
