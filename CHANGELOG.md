# Changelog

## 2.0.0

Ground-up rewrite. **Breaking.**

### Changed
- **Authentication** is now an API token instead of email/password:
  `Labguru(url="https://my.labguru.com", token="...")`. Passing `login`/`password`
  raises `LabguruError`.
- **Transport** is a sync `httpx` client (`LabguruClient(base_url, token)`),
  replacing the previous `requests`-based core.
- **API surface** is namespaced per resource (`lab.projects.list(...)`,
  `lab.protocols.create({...})`, …) instead of flat `lab.list_projects()` methods.
- **Return types** are the API's parsed JSON (`dict`/`list`) rather than typed
  model objects. A `204` response returns `{"success": True}`.
- Packaging moved from `setup.py` to `pyproject.toml` (hatchling). Requires
  Python ≥ 3.9.

### Added
- Resource namespaces: `projects`, `experiments`, `sections`, `elements`,
  `protocols`, `stocks`, `storages`, `tags`, `members` (read-only), `search`
  (read-only; `global_search`), and `biocollections` (with `for_collection` and
  `find_by_external_uuid`).
- `create`/`update` forward arbitrary fields (`external_uuid`, `custom1..N`,
  `tags`), wrapping them under the API's `item` key.
- `LabguruError` / `LabguruAPIError` exception hierarchy.

### Removed
- The `requests`-based modules (`api`, `core`, `response`, `project`, `inventory`,
  `bio`, `error`, `validation`) and the email/password flow.
- The Opentrons example and the 1.x element helpers (`get_elements_by_type`,
  `Element.get_data`, `update_stock_amount`, `add_step`, `add_attachment`) — a
  planned follow-on. See [MIGRATION.md](MIGRATION.md).

> The resource/endpoint shapes are documented but not yet verified against a live
> Labguru instance — see the unverified-assumptions ledger in MIGRATION.md.
