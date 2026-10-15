import json

import httpx
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"


def _lab():
    return Labguru(url=BASE, token="t0k")


@respx.mock
def test_update_text_sends_top_level_data():
    route = respx.put(f"{BASE}/api/v1/elements/9").mock(return_value=httpx.Response(200, json={}))
    _lab().elements.update_text(9, "The updated text")
    assert json.loads(route.calls.last.request.content) == {"data": "The updated text"}


@respx.mock
def test_update_form_sends_form_json_string():
    route = respx.put(f"{BASE}/api/v1/elements/9").mock(return_value=httpx.Response(200, json={}))
    _lab().elements.update_form(9, {"Temperature": "37C"})
    body = json.loads(route.calls.last.request.content)
    assert set(body) == {"form_json"}
    assert json.loads(body["form_json"]) == {"Temperature": "37C"}


@respx.mock
def test_update_does_not_wrap_under_item():
    route = respx.put(f"{BASE}/api/v1/elements/9").mock(return_value=httpx.Response(200, json={}))
    _lab().elements.update(9, {"data": "x"})
    assert json.loads(route.calls.last.request.content) == {"data": "x"}
