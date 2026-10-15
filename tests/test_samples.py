import json

import httpx
import pytest
import respx

from labguru import Labguru
from labguru.exceptions import LabguruError

BASE = "https://demo.labguru.com"
URL = f"{BASE}/api/v1/samples"


def _ns():
    return Labguru(url=BASE, token="t0k").samples


@respx.mock
def test_samples_supported_verbs():
    ns = _ns()
    respx.delete(f"{URL}/1").mock(return_value=httpx.Response(204))
    assert ns.delete(1) == {"success": True}


@pytest.mark.parametrize("verb", ['list', 'get', 'update'])
def test_samples_unsupported_verbs_raise(verb):
    ns = _ns()
    calls = {
        "list": lambda: ns.list(),
        "get": lambda: ns.get(1),
        "update": lambda: ns.update(1, {}),
    }
    with pytest.raises(LabguruError):
        calls[verb]()


@respx.mock
def test_delete_instrument_usage_path():
    route = respx.delete(f"{URL}/3/instrument_usages/8").mock(return_value=httpx.Response(204))
    assert _ns().delete_instrument_usage(3, 8) == {"success": True}
    assert route.called


@respx.mock
def test_link_posts_sample_for_element():
    route = respx.post(URL).mock(return_value=httpx.Response(201, json={"id": 50}))
    assert _ns().link(12, 7, "Catalog::Material") == {"id": 50}
    assert json.loads(route.calls.last.request.content) == {"item": {
        "container_type": "Element", "container_id": 12,
        "item_id": 7, "item_type": "Catalog::Material",
    }}
