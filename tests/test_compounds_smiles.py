import json

import httpx
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"


def _compounds():
    return Labguru(url=BASE, token="t0k").biocollections.for_collection("compounds")


@respx.mock
def test_compounds_create_sends_smiles_beside_item():
    route = respx.post(f"{BASE}/api/v1/compounds").mock(
        return_value=httpx.Response(201, json={"id": 1})
    )
    _compounds().create({"name": "Ethanol"}, smiles="CCO")
    assert json.loads(route.calls.last.request.content) == {
        "smiles": "CCO", "item": {"name": "Ethanol"},
    }


@respx.mock
def test_compounds_update_sends_smiles_beside_item():
    route = respx.put(f"{BASE}/api/v1/compounds/1").mock(
        return_value=httpx.Response(200, json={"id": 1})
    )
    _compounds().update(1, {"cas": "64-17-5"}, smiles="CCO")
    assert json.loads(route.calls.last.request.content) == {
        "smiles": "CCO", "item": {"cas": "64-17-5"},
    }


@respx.mock
def test_create_without_top_level_is_unchanged():
    route = respx.post(f"{BASE}/api/v1/compounds").mock(
        return_value=httpx.Response(201, json={"id": 1})
    )
    _compounds().create({"name": "Ethanol"})
    assert json.loads(route.calls.last.request.content) == {"item": {"name": "Ethanol"}}
