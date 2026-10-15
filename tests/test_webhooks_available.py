import httpx
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"


@respx.mock
def test_available_gets_webhooks_list_endpoint():
    route = respx.get(f"{BASE}/api/v1/webhooks/list").mock(
        return_value=httpx.Response(200, json=[{"name": "experiment.created"}])
    )
    assert Labguru(url=BASE, token="t0k").webhooks.available() == [{"name": "experiment.created"}]
    assert route.calls.last.request.url.params["token"] == "t0k"
