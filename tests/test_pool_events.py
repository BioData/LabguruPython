import json

import httpx
import pytest
import respx

from labguru import Labguru
from labguru.exceptions import LabguruError

BASE = "https://demo.labguru.com"
URL = f"{BASE}/api/v1/pool_events"


def _ns():
    return Labguru(url=BASE, token="t0k").pool_events


@respx.mock
def test_pool_events_create_wraps_under_item():
    route = respx.post(URL).mock(return_value=httpx.Response(200, json={"id": 1}))
    fields = {
        "name": "Pool 1", "pool_type": "fixed", "unit": "mL", "unit_type": "volume",
        "fixed_amount": 1, "stocks_list": [3, 4], "pooled_stock_info": {"name": "Pooled"},
    }
    _ns().create(fields)
    assert json.loads(route.calls.last.request.content) == {"item": fields}


@pytest.mark.parametrize("verb", ["list", "get", "update", "delete"])
def test_pool_events_unsupported_verbs_raise(verb):
    ns = _ns()
    calls = {
        "list": lambda: ns.list(),
        "get": lambda: ns.get(1),
        "update": lambda: ns.update(1, {}),
        "delete": lambda: ns.delete(1),
    }
    with pytest.raises(LabguruError):
        calls[verb]()
