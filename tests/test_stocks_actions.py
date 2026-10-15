import json

import httpx
import respx

from labguru import Labguru

BASE = "https://demo.labguru.com"


def _stocks():
    return Labguru(url=BASE, token="t0k").stocks


@respx.mock
def test_mark_as_consumed_posts_without_body():
    route = respx.post(f"{BASE}/api/v1/stocks/6/mark_as_consumed").mock(
        return_value=httpx.Response(200, json={})
    )
    _stocks().mark_as_consumed(6)
    assert route.calls.last.request.content == b""


@respx.mock
def test_mark_and_unmark_output_send_exp_id():
    mark = respx.post(f"{BASE}/api/v1/stocks/6/mark_as_output").mock(
        return_value=httpx.Response(200, json={})
    )
    unmark = respx.post(f"{BASE}/api/v1/stocks/6/unmark_output").mock(
        return_value=httpx.Response(200, json={})
    )
    _stocks().mark_as_output(6, 11)
    _stocks().unmark_output(6, 11)
    assert json.loads(mark.calls.last.request.content) == {"exp_id": 11}
    assert json.loads(unmark.calls.last.request.content) == {"exp_id": 11}


@respx.mock
def test_update_stock_amount_body():
    route = respx.post(f"{BASE}/api/v1/stocks/6/update_stock_amount").mock(
        return_value=httpx.Response(200, json={})
    )
    _stocks().update_stock_amount(6, 2.5, "mL", unit_type="volume", element_id=40, sample_id=8)
    assert json.loads(route.calls.last.request.content) == {
        "amount_used": "2.5", "unit_type_name": "mL", "subtract": "true",
        "unit_type": "volume", "element_id": 40, "sample_id": 8,
    }


@respx.mock
def test_update_stock_amount_add_back_omits_unset_fields():
    route = respx.post(f"{BASE}/api/v1/stocks/6/update_stock_amount").mock(
        return_value=httpx.Response(200, json={})
    )
    _stocks().update_stock_amount(6, 1, "mg", subtract=False)
    assert json.loads(route.calls.last.request.content) == {
        "amount_used": "1", "unit_type_name": "mg", "subtract": "false",
    }


@respx.mock
def test_find_by_barcode_sends_input_param():
    route = respx.get(f"{BASE}/api/v1/stocks/get_stocks_by_barcode").mock(
        return_value=httpx.Response(200, json=[{"id": 6}])
    )
    assert _stocks().find_by_barcode("BC-001") == [{"id": 6}]
    assert route.calls.last.request.url.params["input"] == "BC-001"
