# labguru/resources/base.py
from __future__ import annotations

from typing import Any, Optional, Union


class BaseResource:
    """CRUD over /api/<api_version>/<resource_name>. Subclasses set `resource_name`
    (and `api_version` for endpoints that only exist under a later API version)."""

    resource_name: str = ""
    api_version: str = "v1"

    def __init__(self, client):
        self.client = client

    def _path(self, suffix: str = "") -> str:
        return f"/api/{self.api_version}/{self.resource_name}{suffix}"

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
