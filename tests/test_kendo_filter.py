import httpx
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"


def _lab():
    return Labguru(url=BASE, token="t0k")


@respx.mock
def test_biocollection_filter_builds_kendo_params():
    route = respx.get(f"{BASE}/api/v1/antibodies").mock(
        return_value=httpx.Response(200, json=[{"id": 1}])
    )
    abs_ = _lab().biocollections.for_collection("antibodies")
    out = abs_.filter([{"field": "title", "operator": "contains", "value": "CD4"}], page=2)
    assert out == [{"id": 1}]
    p = route.calls.last.request.url.params
    assert p["kendo"] == "true"
    assert p["filter[logic]"] == "and"
    assert p["filter[filters][0][field]"] == "title"
    assert p["filter[filters][0][operator]"] == "contains"
    assert p["filter[filters][0][value]"] == "CD4"
    assert p["page"] == "2"


@respx.mock
def test_knowledgebase_filter_with_or_logic_and_tag_ids():
    route = respx.get(f"{BASE}/api/v1/protocols").mock(return_value=httpx.Response(200, json=[]))
    _lab().protocols.filter(
        [{"field": "title", "operator": "startswith", "value": "PCR"},
         {"field": "id", "operator": "eq", "value": 5}],
        logic="or", tag_ids=3,
    )
    p = route.calls.last.request.url.params
    assert p["filter[logic]"] == "or"
    assert p["filter[filters][1][field]"] == "id"
    assert p["filter[filters][1][value]"] == "5"
    assert p["tag_ids"] == "3"


@respx.mock
def test_generic_collection_filter_uses_biocollections_prefix():
    route = respx.get(f"{BASE}/api/v1/biocollections/my_assays").mock(
        return_value=httpx.Response(200, json=[])
    )
    _lab().biocollections.for_generic_collection("my_assays").filter(
        [{"field": "title", "operator": "eq", "value": "A1"}]
    )
    assert route.called
