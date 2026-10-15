import json

import httpx
import pytest
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"


def _req():
    return Labguru(url=BASE, token="t0k").requests


@pytest.mark.parametrize("call, action, body", [
    (lambda r: r.submit(3, name="Assay", team_id=2), "submit",
     {"item": {"name": "Assay", "team_id": 2}}),
    (lambda r: r.approve(3, priority="high"), "approve", {"item": {"priority": "high"}}),
    (lambda r: r.accept(3, priority="low"), "accept", {"item": {"priority": "low"}}),
    (lambda r: r.select_performer(3, 9), "select_performer", {"item": {"performed_by": 9}}),
    (lambda r: r.start(3, performed_by=9), "start", {"item": {"performed_by": 9}}),
])
@respx.mock
def test_transitions_patch_item_body(call, action, body):
    route = respx.patch(f"{BASE}/api/v1/requests/3/{action}").mock(
        return_value=httpx.Response(200, json={"id": 3})
    )
    call(_req())
    assert json.loads(route.calls.last.request.content) == body


@pytest.mark.parametrize("action", ["done", "reject", "submit"])
@respx.mock
def test_bodyless_transitions_send_no_body(action):
    route = respx.patch(f"{BASE}/api/v1/requests/3/{action}").mock(
        return_value=httpx.Response(200, json={"id": 3})
    )
    getattr(_req(), action)(3)
    assert route.calls.last.request.content == b""
    assert route.calls.last.request.url.params["token"] == "t0k"
