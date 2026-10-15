import json

import httpx
import pytest
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"


@pytest.mark.parametrize("ns", ["experiments", "reports"])
@respx.mock
def test_copy_section_posts_item_id_and_section_ids(ns):
    route = respx.post(f"{BASE}/api/v2/{ns}/copy_section").mock(
        return_value=httpx.Response(200, json={})
    )
    getattr(Labguru(url=BASE, token="t0k").v2, ns).copy_section(9, [101, 102])
    assert json.loads(route.calls.last.request.content) == {
        "item": {"item_id": 9, "section_id": [101, 102]},
    }
