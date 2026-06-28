# labguru/client.py
"""Sync HTTP client for the Labguru API."""
from __future__ import annotations

from typing import Any, Optional

import httpx
import json

from labguru.exceptions import LabguruAPIError

_TIMEOUT = 30.0
_UPLOAD_TIMEOUT = 60.0


def build_filter_params(filters: list[dict], prefix: str = "filter[filters]") -> dict:
    """Build Labguru Kendo-style filter query params."""
    params: dict[str, str] = {}
    for i, f in enumerate(filters):
        params[f"{prefix}[{i}][field]"] = f["field"]
        params[f"{prefix}[{i}][operator]"] = f["operator"]
        params[f"{prefix}[{i}][value]"] = str(f["value"])
    return params


class LabguruClient:
    """Sync HTTP client for one Labguru instance. Construct one per instance.

    Each request opens and closes its own ``httpx.Client`` (no connection
    pooling/reuse) — a deliberate simplicity tradeoff for this release.
    """

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def _request(
        self, method: str, path: str, *,
        params: Optional[dict] = None,
        json: Optional[Any] = None,
        data: Optional[dict] = None,
        files: Optional[dict] = None,
        timeout: float = _TIMEOUT,
    ) -> Any:
        request_params = dict(params or {})
        request_params["token"] = self.token
        with httpx.Client() as client:
            resp = client.request(
                method, f"{self.base_url}{path}",
                params=request_params, json=json, data=data, files=files, timeout=timeout,
            )
        if resp.status_code >= 400:
            raise LabguruAPIError(status_code=resp.status_code, message=resp.text)
        if resp.status_code == 204 or not resp.text:
            return {"success": True}
        return resp.json()

    def get(self, path: str, params: Optional[dict] = None) -> Any:
        return self._request("GET", path, params=params)

    def get_with_filters(self, path: str, filters=None, params=None) -> Any:
        request_params = dict(params or {})
        if filters:
            request_params.update(build_filter_params(filters))
        return self.get(path, request_params)

    def post(self, path: str, data: Optional[dict] = None) -> Any:
        return self._request("POST", path, json=data)

    def put(self, path: str, data: Optional[dict] = None) -> Any:
        return self._request("PUT", path, json=data)

    def delete(self, path: str, params: Optional[dict] = None) -> Any:
        return self._request("DELETE", path, params=params)

    def post_form(self, path: str, data: Optional[dict] = None) -> Any:
        """Send form-encoded POST where dict values are JSON-stringified (for endpoints that expect params[:item] as a JSON string)."""
        encoded = {k: json.dumps(v) if isinstance(v, dict)
            else v for k, v in (data or {}).items()}
        return self._request("POST", path, data=encoded)

    def put_form(self, path: str, data: Optional[dict] = None) -> Any:
        """Send form-encoded PUT where dict values are JSON-stringified."""
        encoded = {k: json.dumps(v) if isinstance(v, dict) else v for k, v in (data or {}).items()}
        return self._request("PUT", path, data=encoded)

    def post_multipart(self, path: str, files: dict, data: Optional[dict] = None) -> Any:
        """Multipart upload. files = {field: (filename, bytes)}."""
        return self._request("POST", path, data=data, files=files, timeout=_UPLOAD_TIMEOUT)
