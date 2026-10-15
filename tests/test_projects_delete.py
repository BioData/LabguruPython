import httpx
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"


@respx.mock
def test_projects_delete_uses_v2_endpoint():
    route = respx.delete(f"{BASE}/api/v2/projects/3").mock(return_value=httpx.Response(204))
    assert Labguru(url=BASE, token="t0k").projects.delete(3) == {"success": True}
    assert route.calls.last.request.url.params["token"] == "t0k"
