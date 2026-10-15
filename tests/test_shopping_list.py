import json

import httpx
import pytest
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"
URL = f"{BASE}/api/v1/shopping_list"


def _sl():
    return Labguru(url=BASE, token="t0k").shopping_list


@respx.mock
def test_add_item_and_create_alias_post_to_add_item():
    route = respx.post(f"{URL}/add_item").mock(return_value=httpx.Response(200, json={"id": 1}))
    fields = {"collection_type": "Biocollections::Antibody", "item_id": 3, "quantity": 2}
    _sl().add_item(fields)
    assert json.loads(route.calls.last.request.content) == {"item": fields}
    _sl().create(fields)
    assert route.call_count == 2


@respx.mock
def test_crud_paths():
    respx.get(URL).mock(return_value=httpx.Response(200, json=[]))
    respx.get(f"{URL}/1").mock(return_value=httpx.Response(200, json={"id": 1}))
    upd = respx.put(f"{URL}/1").mock(return_value=httpx.Response(200, json={"id": 1}))
    respx.delete(f"{URL}/1").mock(return_value=httpx.Response(204))
    sl = _sl()
    assert sl.list() == []
    assert sl.get(1) == {"id": 1}
    sl.update(1, {"quantity": 5})
    assert json.loads(upd.calls.last.request.content) == {"item": {"quantity": 5}}
    assert sl.delete(1) == {"success": True}


@pytest.mark.parametrize("action", ["submit", "approve", "cancel"])
@respx.mock
def test_transitions_put_without_body(action):
    route = respx.put(f"{URL}/1/{action}").mock(return_value=httpx.Response(200, json={}))
    getattr(_sl(), action)(1)
    assert route.calls.last.request.content == b""
