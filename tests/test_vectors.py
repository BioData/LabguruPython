import json

import httpx
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"
URL = f"{BASE}/api/v1/vectors"


def _vectors():
    return Labguru(url=BASE, token="t0k").vectors


@respx.mock
def test_vectors_create_sends_top_level_fields():
    route = respx.post(URL).mock(return_value=httpx.Response(201, json={"id": 1}))
    _vectors().create(5, "1,2,3")
    assert json.loads(route.calls.last.request.content) == {"dataset_id": 5, "vector_data": "1,2,3"}


@respx.mock
def test_vectors_update_sends_only_given_fields():
    route = respx.put(f"{URL}/1").mock(return_value=httpx.Response(200, json={"id": 1}))
    _vectors().update(1, vector_data="4,5")
    assert json.loads(route.calls.last.request.content) == {"vector_data": "4,5"}


@respx.mock
def test_vectors_list_get_delete():
    respx.get(URL).mock(return_value=httpx.Response(200, json=[]))
    respx.get(f"{URL}/1").mock(return_value=httpx.Response(200, json={"id": 1}))
    respx.delete(f"{URL}/1").mock(return_value=httpx.Response(204))
    v = _vectors()
    assert v.list() == []
    assert v.get(1) == {"id": 1}
    assert v.delete(1) == {"success": True}
