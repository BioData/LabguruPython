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

Partly restored: `get_elements_by_type` → `lab.experiments.elements(id,
element_type=...)`; `update_stock_amount` → `lab.stocks.update_stock_amount(...)`;
text/form element edits → `lab.elements.update_text` / `update_form`.

Still not ported: `Element.get_data`, `add_step`, `add_attachment` (use
`lab.attachments.create`), and the Opentrons example.

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
- **Generic-collection create wrapping:** the `createGenericItem` schema is empty in the
  spec, so `for_generic_collection(...).create(...)` wrapping under `item` is *inferred
  by analogy* with the other create schemas — confirm via the live smoke test.
- **DELETE coverage:** the 2026-10-15 spec documents DELETE on most resources (it
  was absent from the June spec). The one exception is `projects`, whose delete
  exists only in v2 — `projects.delete` calls `/api/v2/projects/{id}`. See
  [API_GAPS.md](API_GAPS.md).
- **Empty responses:** `204`/empty body → `{"success": True}`.

### Resource support matrix (per the spec, 2026-10-15)

| SDK namespace | list | get | create | update | delete | Notes |
|---|:--:|:--:|:--:|:--:|:--:|---|
| `projects` | ✅ | ✅ | ✅ | ✅ | ✅ | delete via `/api/v2` |
| `milestones` | ✅ | ✅ | ✅ | ✅ | ✅ | folders |
| `experiments` | ✅ | ✅ | ✅ | ✅ | ✅ | + `elements(id)`, `set_flag(id, flag_id)` |
| `protocols` | ✅ | ✅ | ✅ | ✅ | ✅ | form-encoded writes (pending live confirmation) |
| `stocks` | ✅ | ✅ | ✅ | ✅ | ✅ | + consume/output/amount/barcode actions |
| `storages` | ✅ | ✅ | ✅ | ✅ | ✅ | wraps `system_storage_storage` |
| `sections` | ❌ | ✅ | ✅ | ✅ | ✅ | + `sort` |
| `elements` | ❌ | ✅ | ✅ | ✅ | ✅ | `update` unwrapped; + `update_text`/`update_form`/`sort` |
| `tags` | 🚫 | 🚫 | ✅ | 🚫 | ✅ | + `untag` |
| `members` | ✅ | ❌ | 🚫 | 🚫 | 🚫 | `GET /admin/members` only |
| `search` | — | — | 🚫 | 🚫 | 🚫 | `global_search(term, size)` only |
| `biocollections` | ✅ | ✅ | ✅ | ✅ | ✅ | + `filter`, `parents`, `derived_*`; `**top_level` (compounds `smiles`) |
| `datasets` | ✅ | ✅ | ✅ | ❌ | ✅ | |
| `vectors` | ✅ | ✅ | ✅ | ✅ | ✅ | top-level `{dataset_id, vector_data}` |
| `documents` / `notes` / `papers` / `sops` | ✅ | ✅ | ✅ | ✅ | ✅ | |
| `reports` | ✅ | ✅ | ✅ | ✅ | ✅ | + `add_section`, `add_cover` |
| `workflows` | ✅ | ✅ | 🚫 | 🚫 | ✅ | |
| `boxes` / `instruments` | ✅ | ✅ | ✅ | ✅ | ✅ | |
| `units` | ✅ | ✅ | ✅ | ❌ | ✅ | `delete(id, unit_type)` |
| `requests` | ✅ | ✅ | ✅ | ✅ | ✅ | + 7 PATCH transitions |
| `measurements` | 🚫 | 🚫 | ✅ | 🚫 | ✅ | body `{input_name, experiment_id, item}` |
| `visualizations` | 🚫 | 🚫 | ✅ | 🚫 | ✅ | |
| `webhooks` | ✅ | ✅ | ✅ | ✅ | ✅ | + `available()` |
| `attachments` | ❌ | ✅ | ✅ | ✅ | ✅ | multipart `create` |
| `comments` | ✅ | ✅ | ✅ | ❌ | ✅ | |
| `companies` / `events` / `flags` / `links` / `materials` / `request_templates` / `maintenances` / `maintenance_*` | ✅ | ✅ | ✅ | ✅ | ✅ | |
| `plates` | ✅ | ✅ | 🚫 | 🚫 | ✅ | + `find_by_name`, `duplicate` |
| `shopping_list` | ✅ | ✅ | ✅ | ✅ | ✅ | `create` = `add_item`; + submit/approve/cancel |
| `teams` | ✅ | ✅ | 🚫 | 🚫 | ✅ | |
| `manifests` | ✅ | 🚫 | 🚫 | 🚫 | ✅ | |
| `forms` / `recipes` / `signature_flows` | 🚫 | 🚫 | 🚫 | 🚫 | ✅ | delete-only in the spec |
| `samples` | 🚫 | 🚫 | 🚫 | 🚫 | ✅ | + `delete_instrument_usage` |
| `pool_events` | 🚫 | 🚫 | ✅ | 🚫 | 🚫 | |
| `lab.v2.*` | | | | | | experiments (list/create/`copy_section`), reports (`copy_section`), instruments & rodent_cages (list), compound_parent_structures (list/get/update/`compounds`) |

✅ supported · ❌ inherited, no endpoint — runtime `LabguruAPIError(404)` (or
`LabguruError` if the optional "gate undocumented verbs" PR is merged) · 🚫 SDK raises
`LabguruError` before calling.

### Coverage gaps

None remaining against the 2026-10-15 spec except the deliberate omission of
`POST /api/v1/sessions` (email/password → token). See [API_GAPS.md](API_GAPS.md).
