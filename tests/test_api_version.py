import httpx
import respx

from labguru.client import LabguruClient
from labguru.resources.base import BaseResource

BASE = "https://demo.labguru.com"


class _Things(BaseResource):
    resource_name = "things"


@respx.mock
def test_api_version_selects_path_prefix():
    class _V2Things(BaseResource):
        resource_name = "things"
        api_version = "v2"

    client = LabguruClient(BASE, "t0k")
    route = respx.get(f"{BASE}/api/v2/things").mock(return_value=httpx.Response(200, json=[]))
    assert _V2Things(client).list() == []
    assert route.called
    assert _Things(client)._path() == "/api/v1/things"
