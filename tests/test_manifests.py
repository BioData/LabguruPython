import httpx
import pytest
import respx

from labguru import Labguru
from labguru.exceptions import LabguruError

BASE = "https://demo.labguru.com"
URL = f"{BASE}/api/v1/manifests"


def _ns():
    return Labguru(url=BASE, token="t0k").manifests


@respx.mock
def test_manifests_supported_verbs():
    ns = _ns()
    respx.get(URL).mock(return_value=httpx.Response(200, json=[]))
    respx.delete(f"{URL}/1").mock(return_value=httpx.Response(204))
    assert ns.list() == []
    assert ns.delete(1) == {"success": True}


@pytest.mark.parametrize("verb", ['get', 'create', 'update'])
def test_manifests_unsupported_verbs_raise(verb):
    ns = _ns()
    calls = {
        "get": lambda: ns.get(1),
        "create": lambda: ns.create({}),
        "update": lambda: ns.update(1, {}),
    }
    with pytest.raises(LabguruError):
        calls[verb]()
