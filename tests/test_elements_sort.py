import json

import httpx
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"


@respx.mock
def test_elements_sort_posts_container_and_order():
    route = respx.post(f"{BASE}/api/v1/elements/sort").mock(
        return_value=httpx.Response(200, json={})
    )
    Labguru(url=BASE, token="t0k").elements.sort(7, [3, 1, 2])
    assert json.loads(route.calls.last.request.content) == {
        "container_id": 7, "container_type": "Projects::Experiment", "list": [3, 1, 2],
    }
