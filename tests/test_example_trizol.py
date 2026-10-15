"""Runs examples/protocols/create_trizol_rna_isolation.py end to end against a fake
Labguru (respx). Checks the SDK sends the calls the live-verified example in
BioData/labguru-api-examples#4 makes; it does not hit a real instance."""
import importlib
import itertools
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs

import httpx
import pytest
import respx

BASE = "https://demo.labguru.com"
API = f"{BASE}/api/v1"
EXAMPLE_DIR = Path(__file__).resolve().parent.parent / "examples" / "protocols"


@pytest.fixture
def example():
    sys.path.insert(0, str(EXAMPLE_DIR))
    try:
        yield importlib.import_module("create_trizol_rna_isolation")
    finally:
        sys.path.remove(str(EXAMPLE_DIR))


@pytest.fixture
def fake_labguru(example):
    """A stateful fake: returns ids, and records what was created."""
    ids = itertools.count(1000)
    created = {"materials": [], "instruments": [], "elements": []}

    def protocol(request):
        return httpx.Response(200, json={
            "id": 100, "uuid": "uuid-100",
            "experiment_procedures": [
                {"experiment_procedure": {"id": 1, "section_type": "description",
                                          "elements": [{"id": 10, "element_type": "text"}]}},
                {"experiment_procedure": {"id": 2, "section_type": "procedure",
                                          "elements": []}},
            ],
        })

    def section(request):
        sid = int(request.url.path.rsplit("/", 1)[1])
        return httpx.Response(200, json={"id": sid,
                                         "elements": [{"id": 9000 + sid, "element_type": "text"}]})

    def inventory_filter(request):
        name = request.url.params["filter[filters][0][value]"]
        existing = [{"id": 7, "name": "Chloroform"}] if name == "Chloroform" else []
        return httpx.Response(200, json=existing)

    def inventory_create(kind):
        def handler(request):
            item = json.loads(request.content)["item"]
            created[kind].append(item["name"])
            return httpx.Response(201, json=dict(item, id=next(ids)))
        return handler

    def element_create(request):
        item = json.loads(request.content)["item"]
        new = dict(item, id=next(ids))
        created["elements"].append(new)
        return httpx.Response(201, json=new)

    def new_id(status=201):
        return lambda request: httpx.Response(status, json={"id": next(ids)})

    with respx.mock(assert_all_called=False) as mock:
        mock.post(f"{API}/protocols").mock(return_value=httpx.Response(201, json={"id": 100}))
        mock.get(f"{API}/protocols/100").mock(side_effect=protocol)
        mock.delete(f"{API}/protocols/100").mock(return_value=httpx.Response(204))
        mock.post(f"{API}/sections").mock(side_effect=new_id())
        mock.put(url__regex=rf"{API}/sections/\d+").mock(return_value=httpx.Response(200, json={}))
        mock.get(url__regex=rf"{API}/sections/\d+").mock(side_effect=section)
        mock.post(f"{API}/elements").mock(side_effect=element_create)
        mock.get(url__regex=rf"{API}/elements/\d+").mock(
            return_value=httpx.Response(200, json={"data": ""}))
        mock.put(url__regex=rf"{API}/elements/\d+").mock(return_value=httpx.Response(200, json={}))
        mock.delete(url__regex=rf"{API}/elements/\d+").mock(return_value=httpx.Response(204))
        for kind in ("materials", "instruments"):
            mock.get(f"{API}/{kind}").mock(side_effect=inventory_filter)
            mock.post(f"{API}/{kind}").mock(side_effect=inventory_create(kind))
        mock.post(f"{API}/samples").mock(side_effect=new_id())
        mock.post(f"{API}/attachments").mock(side_effect=new_id())
        mock.put(url__regex=rf"{API}/attachments/\d+").mock(
            return_value=httpx.Response(200, json={}))
        mock.get(url__regex=r"https://assets\.thermofisher\.com/.*").mock(
            return_value=httpx.Response(200, content=b"%PDF-1.4 fake"))
        yield mock, created


def _calls(mock, method, pattern):
    def url(call):
        return str(call.request.url.copy_with(query=None))

    return [c for c in mock.calls
            if c.request.method == method and re.fullmatch(pattern, url(c))]


def test_example_builds_the_full_protocol(example, fake_labguru):
    mock, created = fake_labguru
    from trizol_protocol_content import EQUIPMENT, MANUALS, PROCEDURE_SECTIONS, REAGENTS

    assert example.main(url=BASE, token="t0k") == 0

    # Protocol created with the item sent as a JSON string
    create = _calls(mock, "POST", rf"{API}/protocols")[0].request
    assert json.loads(parse_qs(create.content.decode())["item"][0])["name"] == example.PROTOCOL_NAME

    # Description filled through the top-level `data` element update
    description = _calls(mock, "PUT", rf"{API}/elements/10")[0].request
    assert json.loads(description.content) == {"data": example.DESCRIPTION_HTML}

    # Default Procedure section renamed; one new section per stage + the manuals section
    rename = json.loads(_calls(mock, "PUT", rf"{API}/sections/2")[0].request.content)
    assert rename["item"]["name"] == "Materials and equipment"
    assert len(_calls(mock, "POST", rf"{API}/sections")) == len(PROCEDURE_SECTIONS) + 1

    # Inventory: the existing "Chloroform" is reused, everything else is created
    assert "Chloroform" not in created["materials"]
    assert len(created["materials"]) == len(REAGENTS) - 1
    assert len(created["instruments"]) == len(EQUIPMENT)

    # Every reagent and instrument is linked through POST /samples
    links = [json.loads(c.request.content)["item"] for c in _calls(mock, "POST", rf"{API}/samples")]
    assert len(links) == len(REAGENTS) + len(EQUIPMENT)
    assert {link["item_type"] for link in links} == {"Catalog::Material", "System::Instrument"}

    # The samples element's data lists the linked reagents, sent as a JSON string
    samples_el = next(e for e in created["elements"] if e["element_type"] == "samples")
    data_put = _calls(mock, "PUT", rf"{API}/elements/{samples_el['id']}")[0].request
    data = json.loads(json.loads(data_put.content)["data"])
    assert [s["name"] for s in data["samples"]] == [r["name"] for r in REAGENTS]

    # Each manual is uploaded to the protocol and moved into the attachments element
    uploads = _calls(mock, "POST", rf"{API}/attachments")
    assert len(uploads) == len(MANUALS)
    assert b'name="item[attach_to_uuid]"' in uploads[0].request.content
    attachments_el = next(e for e in created["elements"] if e["element_type"] == "attachments")
    moves = _calls(mock, "PUT", rf"{API}/attachments/\d+")
    assert [json.loads(m.request.content) for m in moves] == (
        [{"item": {"element_id": attachments_el["id"]}}] * len(MANUALS))

    # Steps elements store their steps as a JSON string
    step_els = [e for e in created["elements"] if e["element_type"] == "steps"]
    assert all(isinstance(json.loads(e["data"]), list) for e in step_els)

    assert not _calls(mock, "DELETE", rf"{API}/protocols/100")


def test_example_deletes_the_half_built_protocol_on_failure(example, fake_labguru):
    mock, _ = fake_labguru
    mock.post(f"{API}/attachments").mock(return_value=httpx.Response(500, text="boom"))

    assert example.main(url=BASE, token="t0k") == 1
    assert len(_calls(mock, "DELETE", rf"{API}/protocols/100")) == 1
