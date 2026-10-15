import httpx
import pytest
import respx

from labguru import Labguru
from labguru.exceptions import LabguruError

BASE = "https://demo.labguru.com"


def _ns():
    return Labguru(url=BASE, token="t0k").v2.rodent_cages


@respx.mock
def test_v2_rodent_cages_list_with_paging():
    route = respx.get(f"{BASE}/api/v2/rodent_cages").mock(return_value=httpx.Response(200, json=[]))
    assert _ns().list(page=1, page_size=100) == []
    params = route.calls.last.request.url.params
    assert params["page"] == "1"
    assert params["page_size"] == "100"


@pytest.mark.parametrize("verb", ["get", "create", "update", "delete"])
def test_v2_rodent_cages_other_verbs_raise(verb):
    with pytest.raises(LabguruError):
        getattr(_ns(), verb)(1)
