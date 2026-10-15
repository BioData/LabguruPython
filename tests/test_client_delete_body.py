import json

import httpx
import respx

from labguru.client import LabguruClient

BASE = "https://demo.labguru.com"


@respx.mock
def test_delete_sends_optional_json_body():
    route = respx.delete(f"{BASE}/api/v1/units/4").mock(return_value=httpx.Response(204))
    LabguruClient(BASE, "t0k").delete("/api/v1/units/4", data={"unit_type": "weight"})
    sent = route.calls.last.request
    assert sent.url.params["token"] == "t0k"
    assert json.loads(sent.content) == {"unit_type": "weight"}


@respx.mock
def test_delete_without_data_sends_no_body():
    route = respx.delete(f"{BASE}/api/v1/units/4").mock(return_value=httpx.Response(204))
    LabguruClient(BASE, "t0k").delete("/api/v1/units/4")
    assert route.calls.last.request.content == b""
