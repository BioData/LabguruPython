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

## Unverified-assumptions ledger

The 2.0 transport and resource shapes were ported from an existing client and the
plan's reading of the Labguru API. **The test suite uses `respx` mocks, which
verify that the SDK *sends* what we expect — not that the live API *accepts* it.**
The following are best-guess defaults that should be confirmed against a live
Labguru instance (or the Rails API controllers) before relying on them in
production. Until then, treat each as provisional.

- **Auth transport:** token is sent as a `token` query parameter on every request
  (no `Authorization` header).
- **Endpoint paths:** `/api/v1/<resource>` with the pluralized names used here
  (`projects`, `protocols`, `experiments`, `sections`, `elements`, `members`,
  `tags`, `stocks`, `storages`, `searches`) and biocollection names
  (e.g. `plasmids`).
- **Write body wrapping:** create/update payloads are wrapped under an `item` key
  for **all** resources. (Confirmed by the plan for `protocols`; assumed for the
  rest.)
- **`global_search`:** path `/api/v1/searches/global_search`, query parameter name
  `term` (vs. `q` — unconfirmed).
- **`searches` is read-only:** the SDK blocks `create`/`update`/`delete` on
  `lab.search`. Assumed from intent (only `global_search` is defined); not verified
  against the API.
- **`members` is read-only:** index/show only; the SDK blocks writes.
- **External-uuid lookup:** biocollection index endpoints support server-side
  filtering by `external_uuid` (the cross-instance re-discovery story depends on
  this).
- **Sub-resource endpoints:** `GET /api/v1/protocols/{id}/tags` and
  `GET /api/v1/storages/{id}/boxes`.
- **Empty responses:** `204` or an empty body is treated as `{"success": True}`.
