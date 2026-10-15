import json

import httpx
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"


@respx.mock
def test_untag_sends_item_body_to_collection_path():
    route = respx.delete(f"{BASE}/api/v1/tags").mock(return_value=httpx.Response(204))
    lab = Labguru(url=BASE, token="t0k")
    assert lab.tags.untag("Projects::Experiment", 12, "draft,wip") == {"success": True}
    assert json.loads(route.calls.last.request.content) == {
        "item": {"class_name": "Projects::Experiment", "item_id": 12, "tag": "draft,wip"},
    }
