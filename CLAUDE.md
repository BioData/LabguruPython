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
   request (deliberate: no connection pooling). `get_with_filters` builds Kendo-style
   `filter[filters][i][...]` params via `build_filter_params`.

2. **`resources/base.py` — `BaseResource`.** CRUD over `/api/v1/<resource_name>`:
   `list(page=, **params)`, `get(id)`, `create(data)`, `update(id, data)`,
   `delete(id)`. Each method just returns the client's parsed-JSON result. Subclasses
   set `resource_name`.

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

### `facade.py` — the `Labguru` entry point

Constructor takes `url` + `token`. It rejects legacy `login`/`password` kwargs
(raising `LabguruError`) *before* the falsy `url`/`token` check, and instantiates
one resource namespace per attribute (`lab.protocols`, `lab.experiments`,
`lab.projects`, …). Users only touch `Labguru`.

### Resource specifics

- **Read-only resources** (`members`, `search`) override the inherited write methods
  to raise `LabguruError`. `search` adds `global_search(term)`; its inherited
  `list`/`get` are left in place (write methods are what's blocked).
- **`biocollections`** is addressed by collection name: `for_collection(name)`
  returns a new instance with `resource_name = name`; `find_by_external_uuid(uuid)`
  filters the collection index by `external_uuid`.
- **Sub-resource endpoints:** `ProtocolsResource.tags(id)` →
  `/protocols/{id}/tags`; `StoragesResource.boxes(id)` → `/storages/{id}/boxes`.

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
