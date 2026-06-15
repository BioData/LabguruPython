# tests/test_client.py
import json

import httpx
import pytest
import respx

from labguru.client import LabguruClient, build_filter_params
from labguru.exceptions import LabguruAPIError, LabguruError

BASE = "https://demo.labguru.com"


def test_api_error_carries_status_and_message():
    err = LabguruAPIError(status_code=422, message="bad fields")
    assert err.status_code == 422
    assert "bad fields" in str(err)
    assert isinstance(err, LabguruError)


@respx.mock
def test_get_injects_token_and_returns_json():
    resp = httpx.Response(200, json=[{"id": 1}])
    route = respx.get(f"{BASE}/api/v1/projects").mock(return_value=resp)
    out = LabguruClient(BASE, token="t0k").get("/api/v1/projects")
    assert out == [{"id": 1}]
    assert route.calls.last.request.url.params["token"] == "t0k"


@respx.mock
def test_post_sends_json_body_and_token():
    resp = httpx.Response(201, json={"id": 9})
    route = respx.post(f"{BASE}/api/v1/protocols").mock(return_value=resp)
    out = LabguruClient(BASE, token="t0k").post("/api/v1/protocols", {"item": {"title": "x"}})
    assert out == {"id": 9}
    sent = route.calls.last.request
    assert sent.url.params["token"] == "t0k"
    assert json.loads(sent.content)["item"]["title"] == "x"


@respx.mock
def test_error_status_raises():
    respx.get(f"{BASE}/api/v1/projects/999").mock(return_value=httpx.Response(404, text="nope"))
    with pytest.raises(LabguruAPIError) as ei:
        LabguruClient(BASE, "t0k").get("/api/v1/projects/999")
    assert ei.value.status_code == 404


@respx.mock
def test_delete_204_returns_success():
    respx.delete(f"{BASE}/api/v1/tags/3").mock(return_value=httpx.Response(204))
    assert LabguruClient(BASE, "t0k").delete("/api/v1/tags/3") == {"success": True}


def test_build_filter_params_produces_kendo_style_dict():
    filters = [{"field": "name", "operator": "eq", "value": 5}]
    result = build_filter_params(filters)
    assert result["filter[filters][0][field]"] == "name"
    assert result["filter[filters][0][operator]"] == "eq"
    assert result["filter[filters][0][value]"] == "5"


@respx.mock
def test_get_with_filters_passes_token_and_filter_params():
    resp = httpx.Response(200, json=[])
    route = respx.get(f"{BASE}/api/v1/plasmids").mock(return_value=resp)
    LabguruClient(BASE, "t0k").get_with_filters(
        "/api/v1/plasmids",
        filters=[{"field": "name", "operator": "eq", "value": "x"}],
    )
    params = route.calls.last.request.url.params
    assert params["token"] == "t0k"
    assert params["filter[filters][0][field]"] == "name"
    assert params["filter[filters][0][operator]"] == "eq"
    assert params["filter[filters][0][value]"] == "x"
