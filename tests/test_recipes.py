import httpx
import pytest
import respx

from labguru import Labguru
from labguru.exceptions import LabguruError

BASE = "https://demo.labguru.com"
URL = f"{BASE}/api/v1/recipes"


def _ns():
    return Labguru(url=BASE, token="t0k").recipes


@respx.mock
def test_recipes_supported_verbs():
    ns = _ns()
    respx.delete(f"{URL}/1").mock(return_value=httpx.Response(204))
    assert ns.delete(1) == {"success": True}


@pytest.mark.parametrize("verb", ['list', 'get', 'create', 'update'])
def test_recipes_unsupported_verbs_raise(verb):
    ns = _ns()
    calls = {
        "list": lambda: ns.list(),
        "get": lambda: ns.get(1),
        "create": lambda: ns.create({}),
        "update": lambda: ns.update(1, {}),
    }
    with pytest.raises(LabguruError):
        calls[verb]()
