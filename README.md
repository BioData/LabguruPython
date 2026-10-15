# LabguruPython

The official Python SDK for the [Labguru](https://www.labguru.com/) API.

API reference: <https://my.labguru.com/api/docs/>

## Requirements

- Python ≥ 3.9
- An API token from your Labguru account settings

## Installation

```bash
pip install labguru
```

Or from source:

```bash
git clone https://github.com/BioData/LabguruPython.git
cd LabguruPython
pip install -e ".[dev]"
```

## Quickstart

```python
from labguru import Labguru

lab = Labguru(url="https://my.labguru.com", token="YOUR_API_TOKEN")

# List the first page of protocols
print(lab.protocols.list(page=1))

# Create a protocol — arbitrary fields are passed straight through
lab.protocols.create({"name": "My protocol", "external_uuid": "abc"})
```

> **Upgrading from 1.x?** Authentication changed from email/password to an API
> token, and calls are now namespaced (`lab.list_projects()` → `lab.projects.list()`).
> See [MIGRATION.md](MIGRATION.md).

## Usage

A `Labguru` instance exposes one namespace per resource. Each namespace provides
`list(page=…, **filters)`, `get(id)`, `create(fields)`, `update(id, fields)`, and
`delete(id)` (where the API supports them). Every method returns parsed JSON
(`dict` or `list`); a `204 No Content` response returns `{"success": True}`.

The namespaces, by area:

| Area | Namespaces |
|---|---|
| Experiments & knowledge | `projects`, `milestones` (folders), `experiments`, `sections`, `elements`, `protocols`, `datasets`, `vectors` (dataset vectors), `documents`, `notes`, `papers`, `reports`, `sops`, `recipes`, `forms`, `workflows`, `flags`, `links` |
| Inventory & storage | `biocollections`, `stocks`, `samples`, `pool_events`, `storages`, `boxes`, `plates`, `manifests`, `instruments`, `maintenances`, `maintenance_types`, `maintenance_templates`, `maintenance_events`, `materials` (consumables), `companies`, `units` |
| Workflow & collaboration | `requests`, `request_templates`, `shopping_list`, `events`, `measurements`, `visualizations`, `webhooks`, `attachments`, `comments`, `tags`, `members`, `teams`, `signature_flows`, `search` |
| API v2 only | `lab.v2.experiments`, `lab.v2.reports`, `lab.v2.instruments`, `lab.v2.rodent_cages`, `lab.v2.compound_parent_structures` |

Notable shapes (the rest are standard CRUD):

| Namespace | Notes |
|---|---|
| `lab.sections` / `lab.elements` | no `list()` (no collection index); list elements with `experiments.elements(id, element_type=…)`; both have `sort(container_id, ordered_ids)` |
| `lab.elements` | `update_text(id, data)` / `update_form(id, values)` — element updates are **not** wrapped under `item` |
| `lab.storages` | writes wrap under `system_storage_storage` (handled for you) |
| `lab.units` | `delete(id, unit_type)` — `unit_type` is required |
| `lab.tags` | create + delete, plus `untag(class_name, item_id, tag)` |
| `lab.visualizations` | **create + delete only** |
| `lab.workflows` | list / get / delete |
| `lab.measurements` | create + delete: `create(input_name, experiment_id, item)` |
| `lab.requests` | CRUD + `submit` / `approve` / `accept` / `select_performer` / `start` / `done` / `reject` |
| `lab.stocks` | CRUD + `mark_as_consumed`, `mark_as_output`, `unmark_output`, `update_stock_amount`, `find_by_barcode` |
| `lab.projects` | `delete(id)` uses the v2 endpoint |
| `lab.attachments` | `create(files, data=…)` is a **multipart upload**; no `list()` |
| `lab.members` | **read-only**, `list()` only (`GET /api/v1/admin/members`) |
| `lab.search` | `.global_search(term, size=20)` only; writes blocked |
| `lab.biocollections` | `.for_collection(name)` (built-in) / `.for_generic_collection(name)` (custom); `.find_by_external_uuid(uuid)` is **unverified** (see MIGRATION.md) |

> Not every namespace supports every verb — the Labguru API varies by resource. The
> **resource support matrix** in [MIGRATION.md](MIGRATION.md) is the authoritative,
> spec-verified list of exactly what each namespace supports. An unsupported call
> either raises `LabguruError` (blocked client-side) or `LabguruAPIError(404)`.

`create`/`update` take the **inner** payload — the SDK wraps it under the API's
`item` key for you. Pass arbitrary fields (`external_uuid`, `custom1..N`, `tags`)
directly; they are forwarded unchanged.

For server-side filtering use `filter()` (the spec's Kendo filter) on biocollections
and the knowledgebase collections (projects, experiments, protocols, documents,
reports, datasets, papers, sops):

```python
lab.biocollections.for_collection("antibodies").filter(
    [{"field": "title", "operator": "contains", "value": "CD4"}])
lab.protocols.filter([{"field": "title", "operator": "startswith", "value": "PCR"}],
                     tag_ids=3)
```

`list(**params)` sends its kwargs as plain query params (e.g. `meta="true"`);
`search.global_search(term, size=20, model=…, page=…)` likewise passes extras through.

```python
# Work against a named biocollection
plasmids = lab.biocollections.for_collection("plasmids")
plasmids.find_by_external_uuid("external-system-123")

# Two instances? Construct one client each.
source = Labguru(url="https://a.labguru.com", token="TOKEN_A")
target = Labguru(url="https://b.labguru.com", token="TOKEN_B")
```

## Development

```bash
pip install -e ".[dev]"
pytest                      # run the test suite
pytest tests/test_client.py # run a single file
ruff check labguru          # lint
```

Transport unit tests use [`respx`](https://lundberg.github.io/respx/) to mock
httpx. They verify request shaping (URLs, params, body), not a live Labguru
instance — see the unverified-assumptions ledger in [MIGRATION.md](MIGRATION.md).
