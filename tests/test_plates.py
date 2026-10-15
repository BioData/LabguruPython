import json

import httpx
import pytest
import respx

from labguru import Labguru
from labguru.exceptions import LabguruError

BASE = "https://demo.labguru.com"
URL = f"{BASE}/api/v1/plates"


def _plates():
    return Labguru(url=BASE, token="t0k").plates


@respx.mock
def test_plates_list_get_delete():
    respx.get(URL).mock(return_value=httpx.Response(200, json=[]))
    respx.get(f"{URL}/2").mock(return_value=httpx.Response(200, json={"id": 2}))
    respx.delete(f"{URL}/2").mock(return_value=httpx.Response(204))
    p = _plates()
    assert p.list() == []
    assert p.get(2) == {"id": 2}
    assert p.delete(2) == {"success": True}


@respx.mock
def test_find_by_name_sends_name_param():
    route = respx.get(f"{URL}/find_by_name").mock(return_value=httpx.Response(200, json=[]))
    _plates().find_by_name("Plate A")
    assert route.calls.last.request.url.params["name"] == "Plate A"


@respx.mock
def test_duplicate_posts_names():
    route = respx.post(f"{URL}/2/duplicate").mock(return_value=httpx.Response(200, json=[]))
    _plates().duplicate(2, ["Plate B", "Plate C"])
    assert json.loads(route.calls.last.request.content) == {"names": ["Plate B", "Plate C"]}


def test_create_and_update_are_blocked():
    with pytest.raises(LabguruError):
        _plates().create({})
    with pytest.raises(LabguruError):
        _plates().update(2, {})
