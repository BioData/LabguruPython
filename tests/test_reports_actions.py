import json

import httpx
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"


def _lab():
    return Labguru(url=BASE, token="t0k")


@respx.mock
def test_add_section_posts_report_and_section_ids():
    route = respx.post(f"{BASE}/api/v1/reports/add_section_to_report").mock(
        return_value=httpx.Response(201, json={})
    )
    _lab().reports.add_section(5, 77)
    assert json.loads(route.calls.last.request.content) == {
        "item": {"report_id": 5, "section_id": "77"},
    }


@respx.mock
def test_add_cover_posts_cover_data():
    route = respx.post(f"{BASE}/api/v1/reports/add_cover_to_report").mock(
        return_value=httpx.Response(200, json={})
    )
    _lab().reports.add_cover(5, "<h1>Q3</h1>")
    assert json.loads(route.calls.last.request.content) == {
        "item": {"report_id": 5, "data": "<h1>Q3</h1>"},
    }
