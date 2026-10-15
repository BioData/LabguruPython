import json

import httpx
import respx

from labguru.client import LabguruClient

BASE = "https://demo.labguru.com"


@respx.mock
def test_patch_sends_json_body_and_token():
    route = respx.patch(f"{BASE}/api/v1/requests/7/submit").mock(
        return_value=httpx.Response(200, json={"id": 7})
    )
    out = LabguruClient(BASE, "t0k").patch("/api/v1/requests/7/submit", {"item": {"name": "r"}})
    assert out == {"id": 7}
    sent = route.calls.last.request
    assert sent.url.params["token"] == "t0k"
    assert json.loads(sent.content) == {"item": {"name": "r"}}
