# labguru/resources/base.py
from __future__ import annotations

from typing import Any, Optional, Union


class BaseResource:
    """CRUD over /api/v1/<resource_name>. Subclasses set `resource_name`."""

    resource_name: str = ""

    def __init__(self, client):
        self.client = client

    def _path(self, suffix: str = "") -> str:
        return f"/api/v1/{self.resource_name}{suffix}"

    def list(self, page: Optional[int] = None, **params: Any) -> Any:
        if page is not None:
            params["page"] = page
        return self.client.get(self._path(), params=params or None)

    def get(self, resource_id: Union[int, str]) -> Any:
        return self.client.get(self._path(f"/{resource_id}"))

    def create(self, data: dict) -> Any:
        return self.client.post(self._path(), data)

    def update(self, resource_id: Union[int, str], data: dict) -> Any:
        return self.client.put(self._path(f"/{resource_id}"), data)

    def delete(self, resource_id: Union[int, str]) -> Any:
        return self.client.delete(self._path(f"/{resource_id}"))
