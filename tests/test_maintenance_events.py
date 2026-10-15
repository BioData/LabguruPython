import json

import httpx
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"
URL = f"{BASE}/api/v1/maintenance_events"


def _ns():
    return Labguru(url=BASE, token="t0k").maintenance_events


def test_facade_exposes_maintenance_events():
    assert _ns().resource_name == "maintenance_events"


@respx.mock
def test_maintenance_events_crud_paths_and_item_wrapping():
    respx.get(URL).mock(return_value=httpx.Response(200, json=[{"id": 1}]))
    respx.get(f"{URL}/1").mock(return_value=httpx.Response(200, json={"id": 1}))
    create = respx.post(URL).mock(return_value=httpx.Response(201, json={"id": 2}))
    update = respx.put(f"{URL}/2").mock(return_value=httpx.Response(200, json={"id": 2}))
    respx.delete(f"{URL}/2").mock(return_value=httpx.Response(204))
    ns = _ns()
    assert ns.list(page=1) == [{"id": 1}]
    assert ns.get(1) == {"id": 1}
    ns.create({"name": "a", "custom1": "x"})
    assert json.loads(create.calls.last.request.content) == {"item": {"name": "a", "custom1": "x"}}
    ns.update(2, {"name": "b"})
    assert json.loads(update.calls.last.request.content) == {"item": {"name": "b"}}
    assert ns.delete(2) == {"success": True}
