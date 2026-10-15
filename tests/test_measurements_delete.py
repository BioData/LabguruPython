import httpx
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"


@respx.mock
def test_measurements_delete_calls_api():
    route = respx.delete(f"{BASE}/api/v1/measurements/8").mock(return_value=httpx.Response(204))
    assert Labguru(url=BASE, token="t0k").measurements.delete(8) == {"success": True}
    assert route.called
