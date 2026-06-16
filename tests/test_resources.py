import json

import httpx
import pytest
import respx

from labguru.client import LabguruClient
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource

BASE = "https://demo.labguru.com"


class _Things(BaseResource):
    resource_name = "things"


@respx.mock
def test_list_get_create_update_delete():
    client = LabguruClient(BASE, "t0k")
    things = _Things(client)
    respx.get(f"{BASE}/api/v1/things").mock(return_value=httpx.Response(200, json=[{"id": 1}]))
    respx.get(f"{BASE}/api/v1/things/1").mock(return_value=httpx.Response(200, json={"id": 1}))
    respx.post(f"{BASE}/api/v1/things").mock(return_value=httpx.Response(201, json={"id": 2}))
    respx.put(f"{BASE}/api/v1/things/2").mock(
        return_value=httpx.Response(200, json={"id": 2, "name": "n"})
    )
    respx.delete(f"{BASE}/api/v1/things/2").mock(return_value=httpx.Response(204))
    assert things.list() == [{"id": 1}]
    assert things.get(1) == {"id": 1}
    assert things.create({"thing": {"name": "x"}}) == {"id": 2}
    assert things.update(2, {"thing": {"name": "n"}}) == {"id": 2, "name": "n"}
    assert things.delete(2) == {"success": True}


@respx.mock
def test_protocols_create_passes_arbitrary_fields():
    from labguru.resources.protocols import ProtocolsResource
    client = LabguruClient(BASE, "t0k")
    route = respx.post(f"{BASE}/api/v1/protocols").mock(
        return_value=httpx.Response(201, json={"id": 5})
    )
    ProtocolsResource(client).create({"name": "PCR", "external_uuid": "src-123", "custom1": "v"})
    body = json.loads(route.calls.last.request.content)
    assert body["item"]["external_uuid"] == "src-123"
    assert body["item"]["custom1"] == "v"
    assert body["item"]["name"] == "PCR"


@respx.mock
def test_template_resources_wrap_under_item_key():
    from labguru.resources.experiments import ExperimentsResource
    from labguru.resources.projects import ProjectsResource
    client = LabguruClient(BASE, "t0k")
    exp_route = respx.post(f"{BASE}/api/v1/experiments").mock(
        return_value=httpx.Response(201, json={"id": 1})
    )
    route = respx.put(f"{BASE}/api/v1/projects/7").mock(
        return_value=httpx.Response(200, json={"id": 7})
    )
    ExperimentsResource(client).create({"title": "E1"})
    ProjectsResource(client).update(7, {"title": "renamed", "external_uuid": "p-9"})
    exp_body = json.loads(exp_route.calls.last.request.content)
    assert exp_body["item"]["title"] == "E1"
    body = json.loads(route.calls.last.request.content)
    assert body["item"]["title"] == "renamed"
    assert body["item"]["external_uuid"] == "p-9"


@respx.mock
def test_members_is_read_only():
    from labguru.resources.members import MembersResource
    client = LabguruClient(BASE, "t0k")
    members = MembersResource(client)
    respx.get(f"{BASE}/api/v1/admin/members").mock(
        return_value=httpx.Response(200, json=[{"id": 1}])
    )
    assert members.list() == [{"id": 1}]
    for call in (lambda: members.create({"name": "x"}),
                 lambda: members.update(1, {"name": "x"}),
                 lambda: members.delete(1)):
        with pytest.raises(LabguruError):
            call()


@respx.mock
def test_global_search_hits_endpoint():
    from labguru.resources.search import SearchResource
    client = LabguruClient(BASE, "t0k")
    route = respx.get(f"{BASE}/api/v1/searches/global_search").mock(
        return_value=httpx.Response(200, json={"results": []})
    )
    SearchResource(client).global_search("lgcopier:src=abc")
    params = route.calls.last.request.url.params
    assert params["term"] == "lgcopier:src=abc"
    assert params["size"] == "20"  # required by the API; defaulted by the SDK


@respx.mock
def test_biocollections_find_by_external_uuid():
    from labguru.resources.biocollections import BiocollectionsResource
    client = LabguruClient(BASE, "t0k")
    route = respx.get(f"{BASE}/api/v1/plasmids").mock(
        return_value=httpx.Response(200, json=[{"id": 7}])
    )
    out = BiocollectionsResource(client, "plasmids").find_by_external_uuid("src-99")
    assert out == [{"id": 7}]
    assert route.calls.last.request.url.params["external_uuid"] == "src-99"


def test_facade_exposes_namespaces_and_client():
    from labguru import Labguru
    lab = Labguru(url="https://demo.labguru.com", token="t0k")
    assert lab.protocols.resource_name == "protocols"
    assert lab.projects.resource_name == "projects"
    assert lab.client.token == "t0k"


def test_legacy_login_password_is_rejected_with_clear_error():
    from labguru import Labguru
    with pytest.raises(LabguruError) as ei:
        Labguru(login="a@b.com", password="pw")
    assert "token" in str(ei.value).lower()


@respx.mock
def test_biocollections_update_wraps_under_item_key():
    from labguru.resources.biocollections import BiocollectionsResource
    client = LabguruClient(BASE, "t0k")
    route = respx.put(f"{BASE}/api/v1/plasmids/7").mock(
        return_value=httpx.Response(200, json={"id": 7})
    )
    BiocollectionsResource(client, "plasmids").update(7, {"name": "n", "external_uuid": "u"})
    body = json.loads(route.calls.last.request.content)
    assert body["item"]["name"] == "n"
    assert body["item"]["external_uuid"] == "u"


def test_facade_rejects_empty_url():
    from labguru import Labguru
    with pytest.raises(LabguruError):
        Labguru(url="", token="t0k")


def test_facade_rejects_legacy_kwargs_even_with_token():
    from labguru import Labguru
    with pytest.raises(LabguruError) as ei:
        Labguru(url="https://demo.labguru.com", token="t0k", password="pw")
    assert "token" in str(ei.value).lower()


@respx.mock
def test_search_is_read_only():
    from labguru.resources.search import SearchResource
    client = LabguruClient(BASE, "t0k")
    s = SearchResource(client)
    for call in (lambda: s.create({}), lambda: s.update(1, {}), lambda: s.delete(1)):
        with pytest.raises(LabguruError):
            call()


@respx.mock
def test_tags_supports_create_and_delete_only():
    from labguru.resources.tags import TagsResource
    client = LabguruClient(BASE, "t0k")
    tags = TagsResource(client)
    create = respx.post(f"{BASE}/api/v1/tags").mock(
        return_value=httpx.Response(201, json={"id": 1})
    )
    delete = respx.delete(f"{BASE}/api/v1/tags/1").mock(return_value=httpx.Response(204))
    assert tags.create({"name": "x"}) == {"id": 1}
    body = json.loads(create.calls.last.request.content)
    assert body["item"]["name"] == "x"
    assert tags.delete(1) == {"success": True}
    assert delete.called
    for call in (tags.list, lambda: tags.get(1), lambda: tags.update(1, {})):
        with pytest.raises(LabguruError):
            call()
