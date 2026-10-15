import httpx
import pytest
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"


def _bio():
    return Labguru(url=BASE, token="t0k").biocollections


@respx.mock
def test_parents():
    route = respx.get(f"{BASE}/api/v1/cell_lines/4/get_parents").mock(
        return_value=httpx.Response(200, json=[{"id": 1}])
    )
    assert _bio().for_collection("cell_lines").parents(4) == [{"id": 1}]
    assert route.called


@respx.mock
def test_derived_collections():
    route = respx.get(f"{BASE}/api/v1/biocollections/assays/get_derived_collections").mock(
        return_value=httpx.Response(200, json=[])
    )
    _bio().for_generic_collection("assays").derived_collections()
    assert route.called


@respx.mock
def test_derived_items_by_name_and_by_id():
    route = respx.get(f"{BASE}/api/v1/plasmids/4/get_derived_items").mock(
        return_value=httpx.Response(200, json=[])
    )
    plasmids = _bio().for_collection("plasmids")
    plasmids.derived_items(4, derived_collection_name="preps")
    assert route.calls.last.request.url.params["derived_collection_name"] == "preps"
    plasmids.derived_items(4, derived_collection_id=12)
    assert route.calls.last.request.url.params["derived_collection_id"] == "12"


def test_derived_items_requires_name_or_id():
    with pytest.raises(ValueError):
        _bio().for_collection("plasmids").derived_items(4)
