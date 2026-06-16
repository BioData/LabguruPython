# Migrating to labguru 2.0

Version 2.0 is a ground-up rewrite. The public import name is unchanged
(`from labguru import Labguru`), but authentication, the call surface, and the
return types are different.

## Authentication: email/password → API token

```python
# 1.x
lab = Labguru(login="me@example.com", password="...")

# 2.0
lab = Labguru(url="https://my.labguru.com", token="YOUR_API_TOKEN")
```

Passing `login=`/`password=` now raises `LabguruError` with a message pointing you
to the token form. Get a token from your Labguru account settings.

## Calls are namespaced

| 1.x | 2.0 |
|---|---|
| `lab.list_projects(page_num=1)` | `lab.projects.list(page=1)` |
| `lab.get_project("101")` | `lab.projects.get(101)` |
| `lab.add_project(title="x")` | `lab.projects.create({"title": "x"})` |
| `lab.update_project("1", title="x")` | `lab.projects.update(1, {"title": "x"})` |
| `lab.add_inventory_item(name, item_type)` | `lab.biocollections.for_collection(item_type).create({"name": name})` |
| `lab.find_inventory_items(name, item_type)` | `lab.biocollections.for_collection(item_type).list(name=name)` |

## Return types

1.x returned typed model objects (`project.title`). 2.0 returns the API's parsed
JSON directly — a `dict` or `list` of `dict`s. Access fields by key
(`project["title"]`). A `204 No Content` response returns `{"success": True}`.

## Errors

- `LabguruError` — base class for all SDK errors (bad construction, read-only
  violations).
- `LabguruAPIError` — raised on any HTTP status ≥ 400; carries `.status_code` and
  `.message`.

## Not yet ported

The 1.x element helpers (`get_elements_by_type`, `Element.get_data`,
`update_stock_amount`, `add_step`, `add_attachment`) and the Opentrons example
that used them are **not** part of the 2.0 spine. `lab.elements` currently exposes
generic CRUD only. These rich behaviors are a planned follow-on.

## Requirements

Python ≥ 3.9.

---

## API-spec verification ledger

Checked against the Labguru OpenAPI spec
(`https://my.labguru.com/api-docs/v1/swagger.yaml` — OpenAPI 3.0.0, "Labguru API v1",
retrieved 2026-06-16). **Spec-verified ≠ live-verified:** a deployed instance can lag
or extend the published spec, so a live smoke test is still worthwhile — but this is a
large step up from the mock-only confidence the test suite provides.

### Verified ✅
- **Auth:** `token` is a *required* `query` parameter on GET endpoints; the SDK sends
  it as a query param on every request (no `Authorization` header).
- **No `.json` suffix:** endpoints are `/api/v1/<resource>` (the SDK correctly dropped
  the 1.x `.json`).
- **Write wrapping:** create/update bodies are wrapped under an `item` key — confirmed
  on `createProtocol` (body schema = `{token, item}`).
- **`global_search`:** path `/api/v1/searches/global_search`; the search term param is
  `term` (not `q`).
- **CRUD paths** for `projects`, `experiments`, `protocols`, `stocks`, `storages`, and
  named biocollections (`/api/v1/plasmids`, …) match.

### Corrected after spec review 🔧
- **`global_search` requires `size`** (results per page) — was missing; now defaults to
  20 and is overridable for paging.
- **`members` → `/api/v1/admin/members`** (GET index only). The SDK had
  `/api/v1/members`, which does not exist.
- **`tags` = create + delete only** — no list/show/update endpoints exist; the SDK now
  raises on those.
- **Removed `protocols.tags(id)` and `storages.boxes(id)`** — neither
  `/protocols/{id}/tags` nor `/storages/{id}/boxes` exists. (Boxes are a top-level
  `/api/v1/boxes` resource, not a sub-resource.)

### Disproven / unsupported ❌ — needs a product decision
- **`external_uuid` lookup has no documented API support.** The string `external_uuid`
  appears **nowhere** in the spec. The named-collection index documents only
  `page`/`meta`; server-side filtering goes through the Kendo endpoint
  `/api/v1/{collection_name}` (requires `kendo`, `filter[logic]`, and
  `filter[filters][i][field|operator|value]`). `biocollections.find_by_external_uuid`
  is left in place but flagged UNVERIFIED in its docstring — it likely must move to a
  Kendo filter, *and* `external_uuid` must be confirmed to be a filterable field.
- **Cross-instance re-discovery (the lg-copier idempotency story):** all three legs it
  was designed around — `external_uuid`, a protocol `tags` sub-resource, and tag
  *search* — are absent from the spec (`tags` has no GET at all). This affects
  lg-copier's design, not just this SDK.

### Noted but intentionally unchanged
- **Token on writes:** the spec documents `token` in the request *body* for POST/PUT
  (`createProtocol.required: [token]`; write ops declare no query params). The SDK
  sends it as a query param, which the port source (`labguru-mcp`) used successfully
  (Rails merges query and body params). Left as-is; flagged here.
- **`item` as a string:** `createProtocol` documents `item` as a JSON *string*; the SDK
  sends a nested JSON object. Standard Rails nested params accept this.
- **DELETE coverage:** `delete()` is inherited everywhere, but the API supports DELETE
  only on `storages`, `tags`, `events`, `units`, `visualizations`. Elsewhere `delete()`
  raises `LabguruAPIError(404)`. Not gated per-method — see the matrix.
- **Empty responses:** `204`/empty body → `{"success": True}`.

### Resource support matrix (per the spec)

| SDK namespace | list | get | create | update | delete | Notes |
|---|:--:|:--:|:--:|:--:|:--:|---|
| `projects` | ✅ | ✅ | ✅ | ✅ | ❌ | |
| `experiments` | ✅ | ✅ | ✅ | ✅ | ❌ | elements via `GET /experiments/{id}/elements` |
| `protocols` | ✅ | ✅ | ✅ | ✅ | ❌ | |
| `stocks` | ✅ | ✅ | ✅ | ✅ | ❌ | extra actions exist (`update_stock_amount`, …) |
| `storages` | ✅ | ✅ | ✅ | ✅ | ✅ | |
| `sections` | ❌ | ✅ | ✅ | ✅ | ❌ | no collection index |
| `elements` | ❌ | ✅ | ✅ | ✅ | ❌ | list via `GET /experiments/{id}/elements` |
| `tags` | 🚫 | 🚫 | ✅ | 🚫 | ✅ | SDK raises on list/get/update |
| `members` | ✅ | ❌ | 🚫 | 🚫 | 🚫 | `GET /admin/members` only; SDK raises on writes |
| `search` | — | — | 🚫 | 🚫 | 🚫 | `global_search(term, size)` only |
| `biocollections` | ✅ | ✅ | ✅ | ✅ | ❌ | named collections (`/api/v1/<name>`) |

✅ supported · ❌ method exists on the class (inherited) but the endpoint doesn't —
raises `LabguruAPIError(404)` · 🚫 SDK raises `LabguruError` before calling.

### Coverage gaps (in the API, not yet on the facade)
- **`milestones`** (`/api/v1/milestones`) — the 1.x `Folder`. Defensible parity add
  (`lab.folders`); treat as a separate opt-in, not a correctness fix.
- Many standard biocollections already work via
  `lab.biocollections.for_collection(name)` (antibodies, bacteria, cell_lines,
  compounds, genes, primers, proteins, sequences, vectors, viruses, …).
- Not on the facade: `boxes`, `datasets`, `documents`, `instruments`, `notes`,
  `papers`, `reports`, `requests`, `sops`, `units`, `webhooks`, `workflows`,
  `attachments`, `comments`, `measurements`, `visualizations`. Add per need.
