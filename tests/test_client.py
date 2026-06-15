# tests/test_client.py
from labguru.exceptions import LabguruError, LabguruAPIError


def test_api_error_carries_status_and_message():
    err = LabguruAPIError(status_code=422, message="bad fields")
    assert err.status_code == 422
    assert "bad fields" in str(err)
    assert isinstance(err, LabguruError)


import httpx, respx, pytest
from labguru.client import LabguruClient
from labguru.exceptions import LabguruAPIError

BASE = "https://demo.labguru.com"


@respx.mock
def test_get_injects_token_and_returns_json():
    route = respx.get(f"{BASE}/api/v1/projects").mock(return_value=httpx.Response(200, json=[{"id": 1}]))
    out = LabguruClient(BASE, token="t0k").get("/api/v1/projects")
    assert out == [{"id": 1}]
    assert route.calls.last.request.url.params["token"] == "t0k"


@respx.mock
def test_post_sends_json_body_and_token():
    route = respx.post(f"{BASE}/api/v1/protocols").mock(return_value=httpx.Response(201, json={"id": 9}))
    out = LabguruClient(BASE, token="t0k").post("/api/v1/protocols", {"item": {"title": "x"}})
    assert out == {"id": 9}
    import json
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
