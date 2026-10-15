# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`labguru` 2.0 — the official Python SDK for the Labguru REST API
(`https://my.labguru.com/api/v1/...`). API docs: https://my.labguru.com/api/docs/.
The public surface is the single `Labguru` facade; resource classes are internal.

This is a **ground-up rewrite** of the pre-2.0 `requests`/email-password client
(now deleted). If you find references to `api.py`, `core.py`, `response.py`,
`project.py`, `inventory.py`, `bio.py`, `validation.py`, or `Labguru(login=, password=)`,
they are stale.

## Commands

```bash
pip install -e ".[dev]"              # install with dev deps (httpx, pytest, respx, ruff)

pytest                               # run the test suite
pytest tests/test_client.py          # one file
pytest tests/test_resources.py::test_protocols_create_passes_arbitrary_fields  # one test
ruff check labguru                   # lint
```

A local virtualenv lives at `.venv/` (gitignored). Use `.venv/bin/python -m pytest`
and `.venv/bin/ruff` if your shell isn't already in it. Python ≥ 3.9; packaging is
`pyproject.toml` (hatchling) — there is no `setup.py`.

## Architecture

Three layers, all sync:

1. **`client.py` — transport.** `LabguruClient(base_url, token)` wraps `httpx`.
   `_request` injects the **token as a query param** (Labguru uses no Bearer
   header), raises `LabguruAPIError` on status ≥ 400, and returns `{"success": True}`
   for a 204/empty body, else `resp.json()`. A fresh `httpx.Client` is opened per
   request (deliberate: no connection pooling). Verbs: `get`, `post`, `put`,
   `patch`, `delete(path, params=None, data=None)` (DELETE may carry a JSON body —
   `units.delete`, `tags.untag`), `post_form`/`put_form` (form-encoded, dict values
   JSON-stringified — used by `protocols`), `post_multipart`. `get_with_filters`
   builds Kendo-style `filter[filters][i][...]` params via `build_filter_params`.

2. **`resources/base.py` — `BaseResource`.** CRUD over
   `/api/<api_version>/<resource_name>` (`api_version` defaults to `"v1"`):
   `list(page=, **params)`, `get(id)`, `create(data)`, `update(id, data)`,
   `delete(id)`, plus `filter(filters, logic="and", page=None, **params)` — the
   spec's Kendo filter on the collection index, routed through `list()` so a
   resource that blocks `list` also blocks `filter`. Each method just returns the
   client's parsed-JSON result. Subclasses set `resource_name`.

3. **Resource classes (`resources/*.py`) + `facade.py`.**

### Key pattern: create/update wrap under `item_key`

Most resources override `create(fields)` / `update(id, fields)` to wrap the
caller's dict as `{item_key: fields}` (default `item_key = "item"`) before sending,
and pass arbitrary fields through unchanged — so `external_uuid`, `custom1..N`, and
`tags` survive (downstream idempotency depends on this). **Important:** the override
arg is the *inner* payload, not the full body. Passing `{"item": {...}}` would
double-wrap. When you add a write-capable resource, override **both** `create` and
`update` (a past bug: `biocollections` overrode only `create` and inherited an
unwrapped `update`).

**The wrap key is not always `item`** — check the spec schema for every write:
`storages` uses `system_storage_storage`; v2 `compound_parent_structures` uses
`parent_structure`; `elements.update` (`data` / `form_json`), `vectors`
(`dataset_id`, `vector_data`), `stocks.update_stock_amount` and `measurements.create`
send top-level fields; compounds put `smiles` beside `item`
(`biocollections` `create/update(fields, **top_level)`).

### `facade.py` — the `Labguru` entry point

Constructor takes `url` + `token`. It rejects legacy `login`/`password` kwargs
(raising `LabguruError`) *before* the falsy `url`/`token` check, and instantiates
one resource namespace per attribute (`lab.protocols`, `lab.experiments`,
`lab.projects`, …). Endpoints that exist only under `/api/v2` live on a
sub-namespace, `lab.v2.<name>` (`labguru/v2.py`: `experiments`, `reports`,
`instruments`, `rodent_cages`, `compound_parent_structures`), so v1 attributes never
change meaning. Users only touch `Labguru`.

### Resource specifics

- **Restricted resources** (verified against the API spec) override unsupported
  inherited methods to raise `LabguruError`: `members` (`list()` only, at
  `/api/v1/admin/members`); `search` (`global_search(term, size)` only); `tags`
  (create + delete + `untag`); `workflows` (list/get/delete); `measurements` and
  `visualizations` (create + delete); `plates` (no create/update — plates are plate
  elements); `teams`, `manifests`, `forms`, `recipes`, `signature_flows`, `samples`,
  `pool_events`; and the `lab.v2.*` resources.
- **`biocollections`** is addressed by collection name: `for_collection(name)`
  returns a new instance with `resource_name = name`. `find_by_external_uuid(uuid)`
  exists but is **unverified** — `external_uuid` is not in the API spec (see the
  ledger in MIGRATION.md); real filtering uses the Kendo `/{collection_name}` endpoint.
- **Per-verb support varies by resource.** The authoritative endpoint-by-endpoint
  map is [API_GAPS.md](API_GAPS.md); the per-namespace summary is the support matrix
  in [MIGRATION.md](MIGRATION.md).
- **Custom actions** are methods on their namespace, e.g. `requests.submit/approve/
  accept/select_performer/start/done/reject` (PATCH), `stocks.mark_as_consumed /
  mark_as_output / unmark_output / update_stock_amount / find_by_barcode`,
  `experiments.elements / set_flag`, `elements.sort`, `sections.sort`,
  `reports.add_section / add_cover`, `webhooks.available`, `shopping_list.add_item /
  submit / approve / cancel`, `plates.find_by_name / duplicate`, biocollection
  `parents / derived_collections / derived_items`. `projects.delete` calls the v2
  endpoint (v1 has none).
- **The facade exposes 48 v1 namespaces plus `lab.v2`** (wired in `facade.py`), each shaped to the
  verbs the spec supports. When adding another: subclass `BaseResource`, set
  `resource_name`, override `create`/`update` for `item`-wrapping, gate verbs the API
  lacks only when the resource is *fundamentally* non-CRUD (read-only / create-only /
  create+delete, like `workflows`/`measurements`/`visualizations`/`tags`); otherwise
  leave the gap to a runtime 404 and record it in the matrix. Specials:
  `measurements.create` uses a custom body; `attachments.create` is a multipart upload.

### Errors (`exceptions.py`)

`LabguruError` (base) and `LabguruAPIError(status_code, message)` for HTTP ≥ 400.

## Testing & the verification boundary

Tests use `pytest` + `respx`, which mock `httpx` and assert **request shaping**
(URL, params, body) — they do **not** hit a live Labguru instance. Green tests
prove the SDK sends what the plan expected, not that the API accepts it. The
endpoint paths, the `item` wrapping, the `global_search` param name (`term`), and
read-only assumptions are **unverified** — see the ledger at the bottom of
[MIGRATION.md](MIGRATION.md) before treating any of them as fact. `tests/conftest.py`
holds a token-scrubbing `vcr_config` for future recorded smoke tests.
