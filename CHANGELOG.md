# Changelog

## Unreleased — spec gap closure (2026-10-15)

Closes the gaps in [API_GAPS.md](API_GAPS.md) against the published spec.

### Fixed (request shapes)
- `storages` writes wrap under `system_storage_storage`.
- `elements.update` sends its body unwrapped; new `update_text` / `update_form`. **Breaking** for callers relying on `item` wrapping.
- `units.delete(id, unit_type)` sends the required `unit_type`. **Breaking** (new required arg).
- `biocollections` `create/update(fields, **top_level)` — compounds `smiles`.
- `projects.delete` uses `DELETE /api/v2/projects/{id}`.
- `workflows.delete` and `measurements.delete` are no longer blocked.

### Added
- Client: `patch()`, DELETE with a JSON body; `BaseResource.api_version`; `BaseResource.filter()` (Kendo).
- Actions: `tags.untag`, `experiments.elements` / `set_flag`, `elements.sort`, `sections.sort`, `reports.add_section` / `add_cover`, request transitions, stock actions, `webhooks.available`, biocollection `parents` / `derived_collections` / `derived_items`.
- Namespaces: `companies`, `events`, `flags`, `links`, `materials`, `milestones`, `request_templates`, `maintenances`, `maintenance_types`, `maintenance_templates`, `maintenance_events`, `vectors`, `plates`, `shopping_list`, `teams`, `manifests`, `forms`, `recipes`, `signature_flows`, `samples`, `pool_events`.
- `lab.v2`: `experiments`, `reports`, `instruments`, `rodent_cages`, `compound_parent_structures`.

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
- 27 resource namespaces covering the documented API surface: `projects`,
  `experiments`, `sections`, `elements`, `protocols`, `datasets`, `documents`,
  `notes`, `papers`, `reports`, `sops`, `workflows`, `biocollections`, `stocks`,
  `storages`, `boxes`, `instruments`, `units`, `requests`, `measurements`,
  `visualizations`, `webhooks`, `attachments`, `comments`, `tags`, `members`,
  `search`. Each is shaped to the verbs the API actually supports (read-only,
  create-only, and create+delete resources block the rest) — see the support matrix
  in [MIGRATION.md](MIGRATION.md).
- `biocollections.for_collection(name)` (built-in) and `for_generic_collection(name)`
  (custom collections, via the `biocollections/` prefix).
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
