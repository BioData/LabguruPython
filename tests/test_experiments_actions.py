import json

import httpx
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"


def _lab():
    return Labguru(url=BASE, token="t0k")


@respx.mock
def test_experiment_elements_filters_by_type_and_name():
    route = respx.get(f"{BASE}/api/v1/experiments/4/elements").mock(
        return_value=httpx.Response(200, json=[{"id": 1}])
    )
    assert _lab().experiments.elements(4, element_type="text", name="Notes") == [{"id": 1}]
    params = route.calls.last.request.url.params
    assert params["element_type"] == "text"
    assert params["name"] == "Notes"


@respx.mock
def test_experiment_elements_without_filters():
    route = respx.get(f"{BASE}/api/v1/experiments/4/elements").mock(
        return_value=httpx.Response(200, json=[])
    )
    _lab().experiments.elements(4)
    assert set(route.calls.last.request.url.params) == {"token"}


@respx.mock
def test_set_flag_posts_flag_id():
    route = respx.post(f"{BASE}/api/v1/experiments/4/set_flag_as").mock(
        return_value=httpx.Response(200, json={"id": 4})
    )
    _lab().experiments.set_flag(4, 2)
    assert json.loads(route.calls.last.request.content) == {"flag_id": 2}
