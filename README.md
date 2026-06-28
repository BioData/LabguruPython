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

The 27 namespaces, by area:

| Area | Namespaces |
|---|---|
| Experiments & knowledge | `projects`, `experiments`, `sections`, `elements`, `protocols`, `datasets`, `documents`, `notes`, `papers`, `reports`, `sops`, `workflows` |
| Inventory & storage | `biocollections`, `stocks`, `storages`, `boxes`, `instruments`, `units` |
| Workflow & collaboration | `requests`, `measurements`, `visualizations`, `webhooks`, `attachments`, `comments`, `tags`, `members`, `search` |

Notable shapes (the rest are standard CRUD):

| Namespace | Notes |
|---|---|
| `lab.sections` / `lab.elements` | no `list()` (no collection index); list elements via experiments |
| `lab.tags` / `lab.visualizations` | **create + delete only** |
| `lab.workflows` | **read-only** (list/get) |
| `lab.measurements` | **create only**: `create(input_name, experiment_id, item)` |
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

For Kendo-style server-side filters, drop to the low-level client escape hatch:
`lab.client.get_with_filters(path, filters=[{"field": ..., "operator": ..., "value": ...}])`.
The namespaced `list(**params)` methods send their kwargs as plain query params.

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
