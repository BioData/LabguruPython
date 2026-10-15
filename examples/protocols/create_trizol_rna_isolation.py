"""
Create a Labguru protocol for TRIzol Reagent total RNA isolation, using the labguru SDK.

This is the SDK port of BioData/labguru-api-examples#4, which makes the same calls with
raw `requests`. That version was run end to end against my.labguru.com; this one sends
the same calls through the SDK.

Source: Invitrogen TRIzol Reagent User Guide, Pub. No. MAN0001271 Rev. D
https://assets.thermofisher.com/TFS-Assets/LSG/manuals/trizol_reagent.pdf

The protocol content lives in trizol_protocol_content.py; this file is only the API flow.
Protocol content is reproduced from Thermo Fisher Scientific documentation (MAN0001271),
(c) Thermo Fisher Scientific Inc., for demonstration of the Labguru API only.
Trademarks are the property of Thermo Fisher Scientific and its subsidiaries.
The PDF user guides are not stored in this repo; they are downloaded at run time.

What it does (SDK call -> endpoint):
 1. lab.protocols.create          POST /protocols
 2. lab.protocols.get             GET  /protocols/{id}   (find the default sections)
 3. lab.elements.update_text      PUT  /elements/{id}    (fill the Description text)
 4. lab.sections.create / update  POST /sections, PUT /sections/{id}
 5. lab.elements.delete           remove the empty text element each new section gets
 6. lab.elements.create           add "steps", "text", "samples", "equipment", "attachments"
 7. lab.materials / instruments   .filter() to find by name, else .create()
 8. lab.samples.link              POST /samples, then lab.elements.update writes the
                                  element's data so the linked items show in its table
 9. lab.attachments.create        upload the PDFs to the protocol, then
    lab.attachments.update        move them into the attachments element

Usage:
    export LABGURU_TOKEN=...
    python examples/protocols/create_trizol_rna_isolation.py [https://my.labguru.com]

Re-running creates a new protocol but reuses reagents and equipment with the same name.
If a run fails partway, the half-built protocol is deleted (or its URL is printed).
"""
import json
import os
import sys

import httpx

from labguru import Labguru, LabguruError
from trizol_protocol_content import (
    DESCRIPTION_HTML,
    EQUIPMENT,
    MANUALS,
    PROCEDURE_SECTIONS,
    PROTOCOL_NAME,
    REAGENTS,
)

DOWNLOAD_TIMEOUT = 120  # seconds, for the Thermo Fisher PDFs
PROTOCOL_CONTAINER = "Knowledgebase::Protocol"


def text(name, html):
    return {"element_type": "text", "name": name, "data": html}


def steps(name, step_list):
    # A steps element stores its data as a JSON string of step objects
    return {"element_type": "steps", "name": name, "data": json.dumps(step_list)}


def default_sections(lab, protocol_id):
    """{section_type: section} for the sections Labguru creates with a new protocol."""
    protocol = lab.protocols.get(protocol_id)
    sections = [s["experiment_procedure"] for s in protocol.get("experiment_procedures", [])]
    return {s["section_type"]: s for s in sections}


def add_section(lab, protocol_id, name, position):
    section = lab.sections.create({
        "name": name, "container_id": protocol_id,
        "container_type": PROTOCOL_CONTAINER, "position": position,
    })
    print(f"Section '{name}' created. ID: {section['id']}")
    return section["id"]


def add_element(lab, section_id, element):
    created = lab.elements.create(
        dict(element, container_id=section_id, container_type="ExperimentProcedure")
    )
    print(f"  {element['element_type']} element '{element['name']}' added. ID: {created['id']}")
    return created["id"]


def remove_empty_text_elements(lab, section_id):
    """New sections come with an empty text element. Call this before adding content."""
    for element in lab.sections.get(section_id).get("elements", []):
        if element["element_type"] == "text" and not lab.elements.get(element["id"]).get("data"):
            lab.elements.delete(element["id"])
            print(f"  Empty placeholder element {element['id']} removed.")


def find_or_create(namespace, item):
    """Return the inventory item with this exact name, or create it.

    filter() matches on the server, so the whole inventory isn't paged through. The
    name is checked again here in case a server ignores the filter.
    """
    results = namespace.filter([{"field": "name", "operator": "eq", "value": item["name"]}])
    if not isinstance(results, list):
        raise LabguruError(f"{namespace.resource_name} filter returned {str(results)[:200]}")
    matches = [r for r in results if r.get("name") == item["name"]]
    if matches:
        print(f"  Using existing {namespace.resource_name} {matches[0]['id']}: {item['name']}")
        return matches[0]
    created = namespace.create(item)
    print(f"  Created {namespace.resource_name} {created['id']}: {item['name']}")
    return created


def link_items(lab, element_id, item_class, collection_name, items):
    """Link inventory items to a samples/equipment element.

    samples.link creates each link; the element's data must then list the samples so
    they show in the element's table. That data is a JSON object sent as a string.
    """
    element = lab.elements.get(element_id)
    raw = element["data"]
    data = raw if isinstance(raw, dict) else json.loads(raw or "{}")
    data.setdefault("headers", {})
    data["samples"] = []
    for item in items:
        sample = lab.samples.link(element_id, item["id"], item_class)
        data["samples"].append({
            "id": sample["id"], "name": item["name"], "url": item.get("url"),
            "collection_name": collection_name, "data": item,
            "item": {"item_class": item_class, "item_id": item["id"],
                     "generic_collection_id": None},
            "container": {"type": "Element", "id": element_id},
            "remarks": None, "properties": [], "stocks": [], "selected_stocks": [],
            "saved_stocks_ids": [], "select_all_stocks": False, "storages": [],
        })
    lab.elements.update(element_id, {"data": json.dumps(data)})
    print(f"  Linked {len(items)} {collection_name.lower()} to element {element_id}.")


def upload_manual(lab, protocol_uuid, filename, url, description):
    pdf = httpx.get(url, timeout=DOWNLOAD_TIMEOUT, follow_redirects=True)
    pdf.raise_for_status()
    attachment = lab.attachments.create(
        files={"item[attachment]": (filename, pdf.content, "application/pdf")},
        data={"item[title]": filename, "item[description]": description,
              "item[attach_to_uuid]": protocol_uuid},
    )
    print(f"  Uploaded {filename}. Attachment ID: {attachment['id']}")
    return attachment["id"]


def build_protocol(lab, protocol_id):
    defaults = default_sections(lab, protocol_id)

    # Description: fill the default section's empty text element (or add one)
    description = defaults.get("description")
    if description:
        texts = [e for e in description["elements"] if e["element_type"] == "text"]
        if texts:
            lab.elements.update_text(texts[0]["id"], DESCRIPTION_HTML)
        else:
            add_element(lab, description["id"], text("Description", DESCRIPTION_HTML))
    else:
        add_element(lab, add_section(lab, protocol_id, "Description", 1),
                    text("Description", DESCRIPTION_HTML))

    # Materials: reuse the default "Procedure" section, link reagents and equipment
    procedure = defaults.get("procedure")
    if procedure:
        section_id = procedure["id"]
        lab.sections.update(section_id, {"name": "Materials and equipment",
                                         "container_id": protocol_id,
                                         "container_type": PROTOCOL_CONTAINER})
    else:
        section_id = add_section(lab, protocol_id, "Materials and equipment", 2)
    remove_empty_text_elements(lab, section_id)

    reagents = [find_or_create(lab.materials, item) for item in REAGENTS]
    element_id = add_element(lab, section_id,
                             {"element_type": "samples", "name": "Reagents", "data": ""})
    link_items(lab, element_id, "Catalog::Material", "Consumables", reagents)

    instruments = [find_or_create(lab.instruments, item) for item in EQUIPMENT]
    element_id = add_element(lab, section_id,
                             {"element_type": "equipment", "name": "Equipment", "data": ""})
    link_items(lab, element_id, "System::Instrument", "Instruments", instruments)

    # Procedure stages
    for index, (name, element_type, content) in enumerate(PROCEDURE_SECTIONS):
        section_id = add_section(lab, protocol_id, name, index + 3)
        remove_empty_text_elements(lab, section_id)
        add_element(lab, section_id,
                    steps(name, content) if element_type == "steps" else text(name, content))

    # Reference manuals: upload the PDFs, then move them into an attachments element
    section_id = add_section(lab, protocol_id, "Reference manuals", len(PROCEDURE_SECTIONS) + 3)
    remove_empty_text_elements(lab, section_id)
    element_id = add_element(lab, section_id, {"element_type": "attachments",
                                               "name": "Thermo Fisher user guides", "data": ""})
    protocol_uuid = lab.protocols.get(protocol_id)["uuid"]
    for filename, url, description in MANUALS:
        attachment_id = upload_manual(lab, protocol_uuid, filename, url, description)
        lab.attachments.update(attachment_id, {"element_id": element_id})


def main(url=None, token=None):
    url = (url or (sys.argv[1] if len(sys.argv) > 1 else "https://my.labguru.com")).rstrip("/")
    token = token or os.environ.get("LABGURU_TOKEN") or input("Enter token: ").strip()
    lab = Labguru(url=url, token=token)

    protocol = lab.protocols.create(
        {"name": PROTOCOL_NAME, "experiment_procedures": [], "elements": []}
    )
    protocol_id = protocol["id"]
    print(f"Protocol created. ID: {protocol_id}")
    protocol_url = f"{url}/knowledge/protocols/{protocol_id}"
    try:
        build_protocol(lab, protocol_id)
    except (LabguruError, httpx.HTTPError) as error:
        # Don't leave a half-built protocol behind. Inventory items are kept;
        # the next run reuses them by name.
        print(f"\nFailed: {error}")
        try:
            lab.protocols.delete(protocol_id)
            print(f"Deleted the half-built protocol {protocol_id}.")
        except (LabguruError, httpx.HTTPError):
            print(f"Could not delete the half-built protocol. Delete it by hand: {protocol_url}")
        return 1
    print(f"\nDone: {protocol_url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
