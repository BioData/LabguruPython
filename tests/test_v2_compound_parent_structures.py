import json

import httpx
import pytest
import respx

from labguru import Labguru
from labguru.exceptions import LabguruError

BASE = "https://demo.labguru.com"
URL = f"{BASE}/api/v2/compound_parent_structures"


def _ns():
    return Labguru(url=BASE, token="t0k").v2.compound_parent_structures


@respx.mock
def test_list_get_and_compounds():
    respx.get(URL).mock(return_value=httpx.Response(200, json=[{"id": 1}]))
    respx.get(f"{URL}/1").mock(return_value=httpx.Response(200, json={"id": 1}))
    respx.get(f"{URL}/1/compounds").mock(return_value=httpx.Response(200, json=[{"id": 7}]))
    ns = _ns()
    assert ns.list() == [{"id": 1}]
    assert ns.get(1) == {"id": 1}
    assert ns.compounds(1) == [{"id": 7}]


@respx.mock
def test_update_wraps_under_parent_structure():
    route = respx.put(f"{URL}/1").mock(return_value=httpx.Response(200, json={"id": 1}))
    _ns().update(1, {"name": "Scaffold A", "owner_id": "5"})
    assert json.loads(route.calls.last.request.content) == {
        "parent_structure": {"name": "Scaffold A", "owner_id": "5"},
    }


@pytest.mark.parametrize("verb", ["create", "delete"])
def test_create_and_delete_raise(verb):
    with pytest.raises(LabguruError):
        getattr(_ns(), verb)(1)
