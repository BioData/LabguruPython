import httpx
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"


@respx.mock
def test_workflows_delete_calls_api():
    route = respx.delete(f"{BASE}/api/v1/workflows/5").mock(return_value=httpx.Response(204))
    assert Labguru(url=BASE, token="t0k").workflows.delete(5) == {"success": True}
    assert route.calls.last.request.url.params["token"] == "t0k"
