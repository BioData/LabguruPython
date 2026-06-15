import httpx
import respx

from labguru.client import LabguruClient
from labguru.resources.base import BaseResource

BASE = "https://demo.labguru.com"


class _Things(BaseResource):
    resource_name = "things"


@respx.mock
def test_list_get_create_update_delete():
    client = LabguruClient(BASE, "t0k")
    things = _Things(client)
    respx.get(f"{BASE}/api/v1/things").mock(return_value=httpx.Response(200, json=[{"id": 1}]))
    respx.get(f"{BASE}/api/v1/things/1").mock(return_value=httpx.Response(200, json={"id": 1}))
    respx.post(f"{BASE}/api/v1/things").mock(return_value=httpx.Response(201, json={"id": 2}))
    respx.put(f"{BASE}/api/v1/things/2").mock(
        return_value=httpx.Response(200, json={"id": 2, "name": "n"})
    )
    respx.delete(f"{BASE}/api/v1/things/2").mock(return_value=httpx.Response(204))
    assert things.list() == [{"id": 1}]
    assert things.get(1) == {"id": 1}
    assert things.create({"thing": {"name": "x"}}) == {"id": 2}
    assert things.update(2, {"thing": {"name": "n"}}) == {"id": 2, "name": "n"}
    assert things.delete(2) == {"success": True}
