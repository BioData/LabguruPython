import json

import httpx
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"


@respx.mock
def test_storages_create_wraps_under_system_storage_storage():
    route = respx.post(f"{BASE}/api/v1/storages").mock(
        return_value=httpx.Response(201, json={"id": 3})
    )
    Labguru(url=BASE, token="t0k").storages.create({"name": "Freezer A", "storage_type_id": 121})
    body = json.loads(route.calls.last.request.content)
    assert body == {"system_storage_storage": {"name": "Freezer A", "storage_type_id": 121}}


@respx.mock
def test_storages_update_wraps_under_system_storage_storage():
    route = respx.put(f"{BASE}/api/v1/storages/3").mock(
        return_value=httpx.Response(200, json={"id": 3})
    )
    Labguru(url=BASE, token="t0k").storages.update(3, {"temperature": -80})
    body = json.loads(route.calls.last.request.content)
    assert body == {"system_storage_storage": {"temperature": -80}}
