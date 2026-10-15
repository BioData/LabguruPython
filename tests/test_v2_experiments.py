import json

import httpx
import pytest
import respx

from labguru import Labguru
from labguru.exceptions import LabguruError

BASE = "https://demo.labguru.com"
URL = f"{BASE}/api/v2/experiments"


def _exp():
    return Labguru(url=BASE, token="t0k").v2.experiments


@respx.mock
def test_v2_experiments_list_passes_paging_and_filters():
    route = respx.get(URL).mock(return_value=httpx.Response(200, json=[]))
    _exp().list(page=2, page_size=50, to_sign="true")
    params = route.calls.last.request.url.params
    assert params["page"] == "2"
    assert params["page_size"] == "50"
    assert params["to_sign"] == "true"


@respx.mock
def test_v2_experiments_create_wraps_under_item():
    route = respx.post(URL).mock(return_value=httpx.Response(201, json={"id": 1}))
    fields = {
        "title": "Run 1", "project_id": 3, "milestone_name": "Q4",
        "sections": [{"title": "Notes", "elements": []}],
    }
    _exp().create(fields)
    assert json.loads(route.calls.last.request.content) == {"item": fields}


@pytest.mark.parametrize("verb", ["get", "update", "delete"])
def test_v2_experiments_other_verbs_raise(verb):
    with pytest.raises(LabguruError):
        getattr(_exp(), verb)(1)
