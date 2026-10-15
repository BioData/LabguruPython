import json

import httpx
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"


@respx.mock
def test_units_delete_sends_unit_type_body():
    route = respx.delete(f"{BASE}/api/v1/units/4").mock(return_value=httpx.Response(204))
    assert Labguru(url=BASE, token="t0k").units.delete(4, "volume") == {"success": True}
    assert json.loads(route.calls.last.request.content) == {"unit_type": "volume"}
