import httpx
import pytest
import respx

from labguru import Labguru
from labguru.exceptions import LabguruError

BASE = "https://demo.labguru.com"
URL = f"{BASE}/api/v1/teams"


def _ns():
    return Labguru(url=BASE, token="t0k").teams


@respx.mock
def test_teams_supported_verbs():
    ns = _ns()
    respx.get(URL).mock(return_value=httpx.Response(200, json=[]))
    respx.get(f"{URL}/1").mock(return_value=httpx.Response(200, json={"id": 1}))
    respx.delete(f"{URL}/1").mock(return_value=httpx.Response(204))
    assert ns.list() == []
    assert ns.get(1) == {"id": 1}
    assert ns.delete(1) == {"success": True}


@pytest.mark.parametrize("verb", ['create', 'update'])
def test_teams_unsupported_verbs_raise(verb):
    ns = _ns()
    calls = {"create": lambda: ns.create({}), "update": lambda: ns.update(1, {})}
    with pytest.raises(LabguruError):
        calls[verb]()
