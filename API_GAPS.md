# API gap map — SDK 2.0 vs. the published Labguru spec

Source: <https://my.labguru.com/api-docs/index.html> →
`/api-docs/v1/swagger.yaml` (169 paths) and `/api-docs/v2/swagger.yaml` (9 paths),
re-pulled **2026-10-15**. Compared against `feat/sdk-relaunch-2.0` @ `18cd83b`.

This **supersedes the "Resource support matrix" in [MIGRATION.md](MIGRATION.md)**,
which was built from the 2026-06-16 spec. The spec has changed since then: most
resources now document `DELETE`, so that matrix's ❌ delete column (and the note
"DELETE only on storages, tags, events, units, visualizations") is out of date.

Like MIGRATION.md, this is **spec-verified, not live-verified**.

## Status — implemented as one PR per gap

| Gap | PR / branch |
|---|---|
| Branch back to green (protocols form tests, ruff) | #25 |
| Client: DELETE body · `patch()` · `api_version` | #27 · #28 · #29 |
| §1 storages wrap · elements.update · units.delete · compounds smiles · tags.untag | #30 · #31 · #32 · #33 · #34 |
| §2 workflows.delete · measurements.delete | #35 · #36 |
| §3 projects.delete → v2 | #37 |
| §3 inherited verbs with no endpoint raise `LabguruError` (optional) | `fix/gate-undocumented-verbs` |
| §4 experiments · sections.sort · elements.sort · reports · requests · stocks · webhooks · Kendo `filter()` · submodules | #38 · #39 · #40 · #41 · #42 · #43 · #44 · #45 · #46 |
| §4 `filter()` respects blocked `list()` | `fix/filter-respects-blocked-list` |
| §5 companies | #47 |
| §5 events, flags, links, materials, milestones, request_templates, maintenance_* (4), vectors, plates, shopping_list, teams, manifests, forms, recipes, signature_flows, samples, pool_events | `feat/ns-<name>` (one PR each) |
| §6 `lab.v2`: experiments → copy_section → instruments → rodent_cages → compound_parent_structures | `feat/v2-*` (stacked) |
| Deliberately not implemented | `POST /api/v1/sessions` (password auth removed in 2.0) |

The sections below describe the gaps as found on 2026-10-15, before these PRs.

## Totals (341 spec operations)

| Status | Ops | Meaning |
|---|--:|---|
| ✅ covered | 102 | a dedicated facade namespace calls it |
| 🟡 via biocollections | 111 | reachable only through `biocollections.for_collection(name)` / `for_generic_collection(name)` |
| 🚫 blocked | 2 | the spec supports it but the SDK raises `LabguruError` |
| ❌ missing | 126 | no SDK method (reachable only through raw `lab.client`) |

The full per-endpoint table is in the [appendix](#appendix--per-endpoint-coverage).

---

## 1. Request bodies that don't match the spec (likely to fail live)

These calls exist but send a body the spec doesn't describe. **Highest priority.**

| SDK call | SDK sends | Spec expects |
|---|---|---|
| `storages.create` / `update` | `{item: {...}}` | `{system_storage_storage: {name, storage_type_id, ...}}`, so the wrap key is different |
| `elements.update` | `{item: {...}}` | top-level `data` (string, for text elements) **or** top-level `form_json` (JSON string, for form elements). No `item` |
| `units.delete(id)` | no body | body `{unit_type: "weight" \| "volume" \| "concentration"}` (required) |
| `biocollections.for_collection("compounds").create` / `update` | `{item: {...}}` | `{smiles, item: {...}}`: `smiles` sits at the **top level**, next to `item` |
| `protocols.create` / `update` (after `18cd83b`) | form-encoded, `item` as a JSON string, on **both** create and update | JSON body; `item` is a **string** on POST but an **object** on PUT |

Notes:
- **protocols:** `18cd83b` presumably reflects what a live instance accepts, which
  would mean the spec is wrong here. Confirm with the commit author before "fixing" it
  either way. That commit also breaks `test_protocols_create_passes_arbitrary_fields`
  (it still expects a JSON body) and adds 2 ruff errors in `client.py`.
- **`tags`:** the spec has **two** deletes. `tags.delete(id)` → `DELETE /tags/{id}`
  is covered. `DELETE /tags` with body `{item: {class_name, item_id, tag}}` (untag an
  item by label, comma-separated labels allowed) has no SDK method.
- **`attachments.create`:** fine. The caller supplies the `item[attachment]`,
  `item[title]`, ... multipart keys, which matches the spec. The docstring shows
  `item[attachable_type]`, which the spec doesn't list (`attach_to_uuid` and
  `description` are listed).
- **Token placement** (query vs. body) is a known, deliberate deviation, recorded in
  MIGRATION.md, "Noted but intentionally unchanged".

## 2. SDK blocks operations the spec supports

| SDK | Blocked | Spec |
|---|---|---|
| `workflows` | `delete` (described as "read-only") | `DELETE /api/v1/workflows/{id}` |
| `measurements` | `delete` (described as "create only") | `DELETE /api/v1/measurements/{id}` |

The descriptions in CLAUDE.md and MIGRATION.md need updating as well.

## 3. SDK methods with no spec endpoint (will 404)

Inherited from `BaseResource` but not in the v1 spec:

| SDK call | Would hit | Note |
|---|---|---|
| `projects.delete` | `DELETE /api/v1/projects/{id}` | exists only as **v2**: `DELETE /api/v2/projects/{id}` |
| `sections.list` | `GET /api/v1/sections` | no index endpoint |
| `elements.list` | `GET /api/v1/elements` | use `GET /experiments/{id}/elements` (not modeled) |
| `datasets.update` | `PUT /api/v1/datasets/{id}` | |
| `units.update` | `PUT /api/v1/units/{id}` | |
| `attachments.list` | `GET /api/v1/attachments` | |
| `comments.update` | `PUT /api/v1/comments/{id}` | |
| `members.get` | `GET /api/v1/admin/members/{id}` | members is index-only |

## 4. Missing sub-actions on resources the SDK already has

| Namespace | Missing endpoints |
|---|---|
| `experiments` | `GET {id}/elements` (filter `element_type`), `POST {id}/set_flag_as` (`flag_id`) |
| `elements`, `sections` | `POST sort` (`container_id`, `container_type`, `list`) |
| `reports` | `POST add_section_to_report`, `POST add_cover_to_report` |
| `requests` | `PATCH {id}/submit`, `approve`, `accept`, `select_performer`, `start`, `done`, `reject` |
| `stocks` | `POST {id}/mark_as_consumed`, `{id}/mark_as_output`, `{id}/unmark_output`, `{id}/update_stock_amount`; `GET get_stocks_by_barcode` (`input`) |
| `webhooks` | `GET list` |
| `tags` | `DELETE /tags` (untag by label, see §1) |
| `search` | `global_search` takes `model`, `page` and `meta`. These already pass through `**params`, but they aren't documented |
| `biocollections` | Kendo filter endpoints `GET /{collection_name}`, `/biocollections/{name}`, `/{knowledgbase_collection}` (`client.get_with_filters` exists, but no resource uses it); submodule lookups `{name}/{id}/get_parents`, `{name}/get_derived_collections`, `{name}/{id}/get_derived_items` (and the `biocollections/` variants) |
| `list()` on all resources | `meta=true/false` is documented on every index. It passes through `**params` but isn't documented in the SDK |

## 5. Resources with no namespace at all

**Full CRUD in the spec:**
`companies`, `events`, `flags`, `links`, `materials` (Consumables),
`milestones` (Folders, the 1.x `Folder`), `maintenances`, `maintenance_events`,
`maintenance_templates`, `maintenance_types`, `request_templates`,
`vectors` (dataset vectors: body `{dataset_id, vector_data}`, **not** a
biocollection, so `for_collection("vectors")` would wrap it incorrectly).

**Partial:**
- `plates`: list, get, delete, `find_by_name`, `{id}/duplicate` (`names[]`)
- `shopping_list`: list, get, update, delete, `add_item`, `{id}/approve|cancel|submit`
- `teams`: list, get, delete
- `manifests`: list, delete
- `pool_events` (Sample Pooling): create only (fixed / custom / consume variants)

**Delete-only in the spec:** `zebrafishes`, `forms`, `recipes`, `samples`,
`signature_flows`, `samples/{sample_id}/instrument_usages/{id}`.

**Deliberately absent:** `POST /sessions` (token from email/password). 2.0 removed
password auth on purpose.

## 6. API v2 (not supported; the client is hard-wired to `/api/v1`)

| Endpoint | Note |
|---|---|
| `GET` / `POST /api/v2/experiments` | v2 experiments |
| `POST /api/v2/experiments/copy_section` | |
| `POST /api/v2/reports/copy_section` | |
| `GET /api/v2/instruments` | |
| `GET /api/v2/rodent_cages` | |
| `GET /api/v2/compound_parent_structures`, `GET`/`PUT .../{id}`, `GET .../{id}/compounds` | new resource |
| `DELETE /api/v2/projects/{id}` | the only project delete (see §3) |

`BaseResource._path` hard-codes `/api/v1/`, so supporting v2 needs a version knob.

## 7. Biocollections reachable only via `for_collection`

These work today through `lab.biocollections.for_collection(name)` (standard
`{item: ...}` wrapping): antibodies, bacteria, cell_lines, compounds (⚠ see §1,
`smiles`), flies, fungi, genes, lipids, plants, plasmids, primers, proteins,
rodent_cages, rodent_specimens, rodent_strains, seeds, sequences, tissues, viruses,
worms, yeasts, zebrafishes (delete only). Custom collections go through
`for_generic_collection(name)`. Whether to add first-class namespaces
(`lab.antibodies`, ...) is an API-design decision, not a correctness gap.

## Suggested order of work

1. Fix §1 body shapes (storages, elements.update, units.delete, compounds) and get
   the `18cd83b` protocols question answered. Bring the branch back to green.
2. Unblock §2 (workflows/measurements delete). Gate or fix the §3 404 methods
   (`projects.delete` → v2).
3. Add the high-value §4 sub-actions: stock actions, request transitions,
   experiment elements, Kendo filtering (this also unblocks a proper
   `find_by_external_uuid`).
4. Add §5 namespaces as needed (milestones/folders, flags, events, plates,
   shopping_list, teams are the likely first asks).
5. Decide on v2 support (§6).
6. Run a live smoke test against a real instance to settle the spec-vs-live questions.

---

## Appendix — per-endpoint coverage

Generated from the spec (✅ covered · 🟡 via biocollections · 🚫 blocked by SDK ·
❌ missing). "Submodules" `POST /{biocollection_name}` and `PUT /{biocollection_name}/{id}`
are the same endpoints that `for_collection(name).create/update` hit.

| Spec tag | Verb | Path | SDK | How |
|---|---|---|:--:|---|
| Antibodies | DELETE | `/api/v1/antibodies/{id}` | 🟡 | biocollections.for_collection('antibodies').delete |
| Antibodies | GET | `/api/v1/antibodies` | 🟡 | biocollections.for_collection('antibodies').list |
| Antibodies | GET | `/api/v1/antibodies/{id}` | 🟡 | biocollections.for_collection('antibodies').get |
| Antibodies | POST | `/api/v1/antibodies` | 🟡 | biocollections.for_collection('antibodies').create |
| Antibodies | PUT | `/api/v1/antibodies/{id}` | 🟡 | biocollections.for_collection('antibodies').update |
| Attachments | DELETE | `/api/v1/attachments/{id}` | ✅ | attachments.delete |
| Attachments | GET | `/api/v1/attachments/{id}` | ✅ | attachments.get |
| Attachments | POST | `/api/v1/attachments` | ✅ | attachments.create |
| Attachments | PUT | `/api/v1/attachments/{id}` | ✅ | attachments.update |
| Authentication | POST | `/api/v1/sessions` | ❌ | no namespace |
| Bacteria | DELETE | `/api/v1/bacteria/{id}` | 🟡 | biocollections.for_collection('bacteria').delete |
| Bacteria | GET | `/api/v1/bacteria` | 🟡 | biocollections.for_collection('bacteria').list |
| Bacteria | GET | `/api/v1/bacteria/{id}` | 🟡 | biocollections.for_collection('bacteria').get |
| Bacteria | POST | `/api/v1/bacteria` | 🟡 | biocollections.for_collection('bacteria').create |
| Bacteria | PUT | `/api/v1/bacteria/{id}` | 🟡 | biocollections.for_collection('bacteria').update |
| Boxes | DELETE | `/api/v1/boxes/{id}` | ✅ | boxes.delete |
| Boxes | GET | `/api/v1/boxes` | ✅ | boxes.list |
| Boxes | GET | `/api/v1/boxes/{id}` | ✅ | boxes.get |
| Boxes | POST | `/api/v1/boxes` | ✅ | boxes.create |
| Boxes | PUT | `/api/v1/boxes/{id}` | ✅ | boxes.update |
| Cell lines | DELETE | `/api/v1/cell_lines/{id}` | 🟡 | biocollections.for_collection('cell_lines').delete |
| Cell lines | GET | `/api/v1/cell_lines` | 🟡 | biocollections.for_collection('cell_lines').list |
| Cell lines | GET | `/api/v1/cell_lines/{id}` | 🟡 | biocollections.for_collection('cell_lines').get |
| Cell lines | POST | `/api/v1/cell_lines` | 🟡 | biocollections.for_collection('cell_lines').create |
| Cell lines | PUT | `/api/v1/cell_lines/{id}` | 🟡 | biocollections.for_collection('cell_lines').update |
| Comments | DELETE | `/api/v1/comments/{id}` | ✅ | comments.delete |
| Comments | GET | `/api/v1/comments` | ✅ | comments.list |
| Comments | GET | `/api/v1/comments/{id}` | ✅ | comments.get |
| Comments | POST | `/api/v1/comments` | ✅ | comments.create |
| Companies | DELETE | `/api/v1/companies/{id}` | ❌ | no namespace |
| Companies | GET | `/api/v1/companies` | ❌ | no namespace |
| Companies | GET | `/api/v1/companies/{id}` | ❌ | no namespace |
| Companies | POST | `/api/v1/companies` | ❌ | no namespace |
| Companies | PUT | `/api/v1/companies/{id}` | ❌ | no namespace |
| Compound Parent Structures | GET | `/api/v2/compound_parent_structures` | ❌ | v2 not supported (client is v1-only) |
| Compound Parent Structures | GET | `/api/v2/compound_parent_structures/{id}` | ❌ | v2 not supported (client is v1-only) |
| Compound Parent Structures | GET | `/api/v2/compound_parent_structures/{id}/compounds` | ❌ | v2 not supported (client is v1-only) |
| Compound Parent Structures | PUT | `/api/v2/compound_parent_structures/{id}` | ❌ | v2 not supported (client is v1-only) |
| Compounds | DELETE | `/api/v1/compounds/{id}` | 🟡 | biocollections.for_collection('compounds').delete |
| Compounds | GET | `/api/v1/compounds` | 🟡 | biocollections.for_collection('compounds').list |
| Compounds | GET | `/api/v1/compounds/{id}` | 🟡 | biocollections.for_collection('compounds').get |
| Compounds | POST | `/api/v1/compounds` | 🟡 | biocollections.for_collection('compounds').create |
| Compounds | PUT | `/api/v1/compounds/{id}` | 🟡 | biocollections.for_collection('compounds').update |
| Consumables | DELETE | `/api/v1/materials/{id}` | ❌ | no namespace |
| Consumables | GET | `/api/v1/materials` | ❌ | no namespace |
| Consumables | GET | `/api/v1/materials/{id}` | ❌ | no namespace |
| Consumables | POST | `/api/v1/materials` | ❌ | no namespace |
| Consumables | PUT | `/api/v1/materials/{id}` | ❌ | no namespace |
| Datasets | DELETE | `/api/v1/datasets/{id}` | ✅ | datasets.delete |
| Datasets | GET | `/api/v1/datasets` | ✅ | datasets.list |
| Datasets | GET | `/api/v1/datasets/{id}` | ✅ | datasets.get |
| Datasets | POST | `/api/v1/datasets` | ✅ | datasets.create |
| Documents | DELETE | `/api/v1/documents/{id}` | ✅ | documents.delete |
| Documents | GET | `/api/v1/documents` | ✅ | documents.list |
| Documents | GET | `/api/v1/documents/{id}` | ✅ | documents.get |
| Documents | POST | `/api/v1/documents` | ✅ | documents.create |
| Documents | PUT | `/api/v1/documents/{id}` | ✅ | documents.update |
| Elements | DELETE | `/api/v1/elements/{id}` | ✅ | elements.delete |
| Elements | GET | `/api/v1/elements/{id}` | ✅ | elements.get |
| Elements | POST | `/api/v1/elements` | ✅ | elements.create |
| Elements | POST | `/api/v1/elements/sort` | ❌ | sub-action on elements (client only) |
| Elements | PUT | `/api/v1/elements/{id}` | ✅ | elements.update |
| Equipment | DELETE | `/api/v1/instruments/{id}` | ✅ | instruments.delete |
| Equipment | GET | `/api/v1/instruments` | ✅ | instruments.list |
| Equipment | GET | `/api/v1/instruments/{id}` | ✅ | instruments.get |
| Equipment | GET | `/api/v2/instruments` | ❌ | v2 not supported (client is v1-only) |
| Equipment | POST | `/api/v1/instruments` | ✅ | instruments.create |
| Equipment | PUT | `/api/v1/instruments/{id}` | ✅ | instruments.update |
| Events | DELETE | `/api/v1/events/{id}` | ❌ | no namespace |
| Events | GET | `/api/v1/events` | ❌ | no namespace |
| Events | GET | `/api/v1/events/{id}` | ❌ | no namespace |
| Events | POST | `/api/v1/events` | ❌ | no namespace |
| Events | PUT | `/api/v1/events/{id}` | ❌ | no namespace |
| Experiments | DELETE | `/api/v1/experiments/{id}` | ✅ | experiments.delete |
| Experiments | GET | `/api/v1/experiments` | ✅ | experiments.list |
| Experiments | GET | `/api/v1/experiments/{id}` | ✅ | experiments.get |
| Experiments | GET | `/api/v1/experiments/{id}/elements` | ❌ | sub-action on experiments (client only) |
| Experiments | GET | `/api/v2/experiments` | ❌ | v2 not supported (client is v1-only) |
| Experiments | POST | `/api/v1/experiments` | ✅ | experiments.create |
| Experiments | POST | `/api/v1/experiments/{id}/set_flag_as` | ❌ | sub-action on experiments (client only) |
| Experiments | POST | `/api/v2/experiments` | ❌ | v2 not supported (client is v1-only) |
| Experiments | POST | `/api/v2/experiments/copy_section` | ❌ | v2 not supported (client is v1-only) |
| Experiments | PUT | `/api/v1/experiments/{id}` | ✅ | experiments.update |
| Filters | GET | `/api/v1/biocollections/{collection_name}` | ❌ | no namespace |
| Filters | GET | `/api/v1/{collection_name}` | ❌ | no namespace |
| Filters | GET | `/api/v1/{knowledgbase_collection}` | ❌ | no namespace |
| Flags | DELETE | `/api/v1/flags/{id}` | ❌ | no namespace |
| Flags | GET | `/api/v1/flags` | ❌ | no namespace |
| Flags | GET | `/api/v1/flags/{id}` | ❌ | no namespace |
| Flags | POST | `/api/v1/flags` | ❌ | no namespace |
| Flags | PUT | `/api/v1/flags/{id}` | ❌ | no namespace |
| Flies | DELETE | `/api/v1/flies/{id}` | 🟡 | biocollections.for_collection('flies').delete |
| Flies | GET | `/api/v1/flies` | 🟡 | biocollections.for_collection('flies').list |
| Flies | GET | `/api/v1/flies/{id}` | 🟡 | biocollections.for_collection('flies').get |
| Flies | POST | `/api/v1/flies` | 🟡 | biocollections.for_collection('flies').create |
| Flies | PUT | `/api/v1/flies/{id}` | 🟡 | biocollections.for_collection('flies').update |
| Folders | DELETE | `/api/v1/milestones/{id}` | ❌ | no namespace |
| Folders | GET | `/api/v1/milestones` | ❌ | no namespace |
| Folders | GET | `/api/v1/milestones/{id}` | ❌ | no namespace |
| Folders | POST | `/api/v1/milestones` | ❌ | no namespace |
| Folders | PUT | `/api/v1/milestones/{id}` | ❌ | no namespace |
| Forms | DELETE | `/api/v1/forms/{id}` | ❌ | no namespace |
| Fungi | DELETE | `/api/v1/fungi/{id}` | 🟡 | biocollections.for_collection('fungi').delete |
| Fungi | GET | `/api/v1/fungi` | 🟡 | biocollections.for_collection('fungi').list |
| Fungi | GET | `/api/v1/fungi/{id}` | 🟡 | biocollections.for_collection('fungi').get |
| Fungi | POST | `/api/v1/fungi` | 🟡 | biocollections.for_collection('fungi').create |
| Fungi | PUT | `/api/v1/fungi/{id}` | 🟡 | biocollections.for_collection('fungi').update |
| Generic Items | DELETE | `/api/v1/biocollections/{generic_collection_name}/{id}` | 🟡 | biocollections.for_generic_collection(n).delete |
| Generic Items | GET | `/api/v1/biocollections/{generic_collection_name}` | 🟡 | biocollections.for_generic_collection(n).list |
| Generic Items | GET | `/api/v1/biocollections/{generic_collection_name}/{id}` | 🟡 | biocollections.for_generic_collection(n).get |
| Generic Items | POST | `/api/v1/biocollections/{generic_collection_name}` | 🟡 | biocollections.for_generic_collection(n).create |
| Generic Items | PUT | `/api/v1/biocollections/{generic_collection_name}/{id}` | 🟡 | biocollections.for_generic_collection(n).update |
| Genes | DELETE | `/api/v1/genes/{id}` | 🟡 | biocollections.for_collection('genes').delete |
| Genes | GET | `/api/v1/genes` | 🟡 | biocollections.for_collection('genes').list |
| Genes | GET | `/api/v1/genes/{id}` | 🟡 | biocollections.for_collection('genes').get |
| Genes | POST | `/api/v1/genes` | 🟡 | biocollections.for_collection('genes').create |
| Genes | PUT | `/api/v1/genes/{id}` | 🟡 | biocollections.for_collection('genes').update |
| Instrument usages | DELETE | `/api/v1/samples/{sample_id}/instrument_usages/{id}` | ❌ | no namespace |
| Links | DELETE | `/api/v1/links/{id}` | ❌ | no namespace |
| Links | GET | `/api/v1/links` | ❌ | no namespace |
| Links | GET | `/api/v1/links/{id}` | ❌ | no namespace |
| Links | POST | `/api/v1/links` | ❌ | no namespace |
| Links | PUT | `/api/v1/links/{id}` | ❌ | no namespace |
| Lipids | DELETE | `/api/v1/lipids/{id}` | 🟡 | biocollections.for_collection('lipids').delete |
| Lipids | GET | `/api/v1/lipids` | 🟡 | biocollections.for_collection('lipids').list |
| Lipids | GET | `/api/v1/lipids/{id}` | 🟡 | biocollections.for_collection('lipids').get |
| Lipids | POST | `/api/v1/lipids` | 🟡 | biocollections.for_collection('lipids').create |
| Lipids | PUT | `/api/v1/lipids/{id}` | 🟡 | biocollections.for_collection('lipids').update |
| Maintenance event | DELETE | `/api/v1/maintenance_events/{id}` | ❌ | no namespace |
| Maintenance event | GET | `/api/v1/maintenance_events` | ❌ | no namespace |
| Maintenance event | GET | `/api/v1/maintenance_events/{id}` | ❌ | no namespace |
| Maintenance event | POST | `/api/v1/maintenance_events` | ❌ | no namespace |
| Maintenance event | PUT | `/api/v1/maintenance_events/{id}` | ❌ | no namespace |
| Maintenance template | DELETE | `/api/v1/maintenance_templates/{id}` | ❌ | no namespace |
| Maintenance template | GET | `/api/v1/maintenance_templates` | ❌ | no namespace |
| Maintenance template | GET | `/api/v1/maintenance_templates/{id}` | ❌ | no namespace |
| Maintenance template | POST | `/api/v1/maintenance_templates` | ❌ | no namespace |
| Maintenance template | PUT | `/api/v1/maintenance_templates/{id}` | ❌ | no namespace |
| Maintenance types | DELETE | `/api/v1/maintenance_types/{id}` | ❌ | no namespace |
| Maintenance types | GET | `/api/v1/maintenance_types` | ❌ | no namespace |
| Maintenance types | GET | `/api/v1/maintenance_types/{id}` | ❌ | no namespace |
| Maintenance types | POST | `/api/v1/maintenance_types` | ❌ | no namespace |
| Maintenance types | PUT | `/api/v1/maintenance_types/{id}` | ❌ | no namespace |
| Maintenances | DELETE | `/api/v1/maintenances/{id}` | ❌ | no namespace |
| Maintenances | GET | `/api/v1/maintenances` | ❌ | no namespace |
| Maintenances | GET | `/api/v1/maintenances/{id}` | ❌ | no namespace |
| Maintenances | POST | `/api/v1/maintenances` | ❌ | no namespace |
| Maintenances | PUT | `/api/v1/maintenances/{id}` | ❌ | no namespace |
| Manifest | DELETE | `/api/v1/manifests/{id}` | ❌ | no namespace |
| Manifest | GET | `/api/v1/manifests` | ❌ | no namespace |
| Measurements | DELETE | `/api/v1/measurements/{id}` | 🚫 | measurements.delete raises LabguruError |
| Measurements | POST | `/api/v1/measurements` | ✅ | measurements.create |
| Members | GET | `/api/v1/admin/members` | ✅ | members.list |
| Notes | DELETE | `/api/v1/notes/{id}` | ✅ | notes.delete |
| Notes | GET | `/api/v1/notes` | ✅ | notes.list |
| Notes | GET | `/api/v1/notes/{id}` | ✅ | notes.get |
| Notes | POST | `/api/v1/notes` | ✅ | notes.create |
| Notes | PUT | `/api/v1/notes/{id}` | ✅ | notes.update |
| Papers | DELETE | `/api/v1/papers/{id}` | ✅ | papers.delete |
| Papers | GET | `/api/v1/papers` | ✅ | papers.list |
| Papers | GET | `/api/v1/papers/{id}` | ✅ | papers.get |
| Papers | POST | `/api/v1/papers` | ✅ | papers.create |
| Papers | PUT | `/api/v1/papers/{id}` | ✅ | papers.update |
| Plants | DELETE | `/api/v1/plants/{id}` | 🟡 | biocollections.for_collection('plants').delete |
| Plants | GET | `/api/v1/plants` | 🟡 | biocollections.for_collection('plants').list |
| Plants | GET | `/api/v1/plants/{id}` | 🟡 | biocollections.for_collection('plants').get |
| Plants | POST | `/api/v1/plants` | 🟡 | biocollections.for_collection('plants').create |
| Plants | PUT | `/api/v1/plants/{id}` | 🟡 | biocollections.for_collection('plants').update |
| Plasmids | DELETE | `/api/v1/plasmids/{id}` | 🟡 | biocollections.for_collection('plasmids').delete |
| Plasmids | GET | `/api/v1/plasmids` | 🟡 | biocollections.for_collection('plasmids').list |
| Plasmids | GET | `/api/v1/plasmids/{id}` | 🟡 | biocollections.for_collection('plasmids').get |
| Plasmids | POST | `/api/v1/plasmids` | 🟡 | biocollections.for_collection('plasmids').create |
| Plasmids | PUT | `/api/v1/plasmids/{id}` | 🟡 | biocollections.for_collection('plasmids').update |
| Plates | DELETE | `/api/v1/plates/{id}` | ❌ | no namespace |
| Plates | GET | `/api/v1/plates` | ❌ | no namespace |
| Plates | GET | `/api/v1/plates/find_by_name` | ❌ | no namespace |
| Plates | GET | `/api/v1/plates/{id}` | ❌ | no namespace |
| Plates | POST | `/api/v1/plates/{id}/duplicate` | ❌ | no namespace |
| Primers | DELETE | `/api/v1/primers/{id}` | 🟡 | biocollections.for_collection('primers').delete |
| Primers | GET | `/api/v1/primers` | 🟡 | biocollections.for_collection('primers').list |
| Primers | GET | `/api/v1/primers/{id}` | 🟡 | biocollections.for_collection('primers').get |
| Primers | POST | `/api/v1/primers` | 🟡 | biocollections.for_collection('primers').create |
| Primers | PUT | `/api/v1/primers/{id}` | 🟡 | biocollections.for_collection('primers').update |
| Projects | DELETE | `/api/v2/projects/{id}` | ❌ | v2 not supported (client is v1-only) |
| Projects | GET | `/api/v1/projects` | ✅ | projects.list |
| Projects | GET | `/api/v1/projects/{id}` | ✅ | projects.get |
| Projects | POST | `/api/v1/projects` | ✅ | projects.create |
| Projects | PUT | `/api/v1/projects/{id}` | ✅ | projects.update |
| Proteins | DELETE | `/api/v1/proteins/{id}` | 🟡 | biocollections.for_collection('proteins').delete |
| Proteins | GET | `/api/v1/proteins` | 🟡 | biocollections.for_collection('proteins').list |
| Proteins | GET | `/api/v1/proteins/{id}` | 🟡 | biocollections.for_collection('proteins').get |
| Proteins | POST | `/api/v1/proteins` | 🟡 | biocollections.for_collection('proteins').create |
| Proteins | PUT | `/api/v1/proteins/{id}` | 🟡 | biocollections.for_collection('proteins').update |
| Protocols | DELETE | `/api/v1/protocols/{id}` | ✅ | protocols.delete |
| Protocols | GET | `/api/v1/protocols` | ✅ | protocols.list |
| Protocols | GET | `/api/v1/protocols/{id}` | ✅ | protocols.get |
| Protocols | POST | `/api/v1/protocols` | ✅ | protocols.create |
| Protocols | PUT | `/api/v1/protocols/{id}` | ✅ | protocols.update |
| Recipes | DELETE | `/api/v1/recipes/{id}` | ❌ | no namespace |
| Reports | DELETE | `/api/v1/reports/{id}` | ✅ | reports.delete |
| Reports | GET | `/api/v1/reports` | ✅ | reports.list |
| Reports | GET | `/api/v1/reports/{id}` | ✅ | reports.get |
| Reports | POST | `/api/v1/reports` | ✅ | reports.create |
| Reports | POST | `/api/v1/reports/add_cover_to_report` | ❌ | sub-action on reports (client only) |
| Reports | POST | `/api/v1/reports/add_section_to_report` | ❌ | sub-action on reports (client only) |
| Reports | POST | `/api/v2/reports/copy_section` | ❌ | v2 not supported (client is v1-only) |
| Reports | PUT | `/api/v1/reports/{id}` | ✅ | reports.update |
| Request templates | DELETE | `/api/v1/request_templates/{id}` | ❌ | no namespace |
| Request templates | GET | `/api/v1/request_templates` | ❌ | no namespace |
| Request templates | GET | `/api/v1/request_templates/{id}` | ❌ | no namespace |
| Request templates | POST | `/api/v1/request_templates` | ❌ | no namespace |
| Request templates | PUT | `/api/v1/request_templates/{id}` | ❌ | no namespace |
| Requests | DELETE | `/api/v1/requests/{id}` | ✅ | requests.delete |
| Requests | GET | `/api/v1/requests` | ✅ | requests.list |
| Requests | GET | `/api/v1/requests/{id}` | ✅ | requests.get |
| Requests | PATCH | `/api/v1/requests/{id}/accept` | ❌ | sub-action on requests (client only) |
| Requests | PATCH | `/api/v1/requests/{id}/approve` | ❌ | sub-action on requests (client only) |
| Requests | PATCH | `/api/v1/requests/{id}/done` | ❌ | sub-action on requests (client only) |
| Requests | PATCH | `/api/v1/requests/{id}/reject` | ❌ | sub-action on requests (client only) |
| Requests | PATCH | `/api/v1/requests/{id}/select_performer` | ❌ | sub-action on requests (client only) |
| Requests | PATCH | `/api/v1/requests/{id}/start` | ❌ | sub-action on requests (client only) |
| Requests | PATCH | `/api/v1/requests/{id}/submit` | ❌ | sub-action on requests (client only) |
| Requests | POST | `/api/v1/requests` | ✅ | requests.create |
| Requests | PUT | `/api/v1/requests/{id}` | ✅ | requests.update |
| Rodent Specimens | DELETE | `/api/v1/rodent_specimens/{id}` | 🟡 | biocollections.for_collection('rodent_specimens').delete |
| Rodent Specimens | GET | `/api/v1/rodent_specimens` | 🟡 | biocollections.for_collection('rodent_specimens').list |
| Rodent Specimens | GET | `/api/v1/rodent_specimens/{id}` | 🟡 | biocollections.for_collection('rodent_specimens').get |
| Rodent Specimens | POST | `/api/v1/rodent_specimens` | 🟡 | biocollections.for_collection('rodent_specimens').create |
| Rodent Specimens | PUT | `/api/v1/rodent_specimens/{id}` | 🟡 | biocollections.for_collection('rodent_specimens').update |
| Rodent Strains | DELETE | `/api/v1/rodent_strains/{id}` | 🟡 | biocollections.for_collection('rodent_strains').delete |
| Rodent Strains | GET | `/api/v1/rodent_strains` | 🟡 | biocollections.for_collection('rodent_strains').list |
| Rodent Strains | GET | `/api/v1/rodent_strains/{id}` | 🟡 | biocollections.for_collection('rodent_strains').get |
| Rodent Strains | POST | `/api/v1/rodent_strains` | 🟡 | biocollections.for_collection('rodent_strains').create |
| Rodent Strains | PUT | `/api/v1/rodent_strains/{id}` | 🟡 | biocollections.for_collection('rodent_strains').update |
| Rodent cages | DELETE | `/api/v1/rodent_cages/{id}` | 🟡 | biocollections.for_collection('rodent_cages').delete |
| Rodent cages | GET | `/api/v1/rodent_cages` | 🟡 | biocollections.for_collection('rodent_cages').list |
| Rodent cages | GET | `/api/v1/rodent_cages/{id}` | 🟡 | biocollections.for_collection('rodent_cages').get |
| Rodent cages | GET | `/api/v2/rodent_cages` | ❌ | v2 not supported (client is v1-only) |
| Rodent cages | POST | `/api/v1/rodent_cages` | 🟡 | biocollections.for_collection('rodent_cages').create |
| Rodent cages | PUT | `/api/v1/rodent_cages/{id}` | 🟡 | biocollections.for_collection('rodent_cages').update |
| SOPs | DELETE | `/api/v1/sops/{id}` | ✅ | sops.delete |
| SOPs | GET | `/api/v1/sops` | ✅ | sops.list |
| SOPs | GET | `/api/v1/sops/{id}` | ✅ | sops.get |
| SOPs | POST | `/api/v1/sops` | ✅ | sops.create |
| SOPs | PUT | `/api/v1/sops/{id}` | ✅ | sops.update |
| Sample Pooling | POST | `/api/v1/pool_events` | ❌ | no namespace |
| Samples | DELETE | `/api/v1/samples/{id}` | ❌ | no namespace |
| Search | GET | `/api/v1/searches/global_search` | ✅ | search.global_search |
| Sections | DELETE | `/api/v1/sections/{id}` | ✅ | sections.delete |
| Sections | GET | `/api/v1/sections/{id}` | ✅ | sections.get |
| Sections | POST | `/api/v1/sections` | ✅ | sections.create |
| Sections | POST | `/api/v1/sections/sort` | ❌ | sub-action on sections (client only) |
| Sections | PUT | `/api/v1/sections/{id}` | ✅ | sections.update |
| Seeds | DELETE | `/api/v1/seeds/{id}` | 🟡 | biocollections.for_collection('seeds').delete |
| Seeds | GET | `/api/v1/seeds` | 🟡 | biocollections.for_collection('seeds').list |
| Seeds | GET | `/api/v1/seeds/{id}` | 🟡 | biocollections.for_collection('seeds').get |
| Seeds | POST | `/api/v1/seeds` | 🟡 | biocollections.for_collection('seeds').create |
| Seeds | PUT | `/api/v1/seeds/{id}` | 🟡 | biocollections.for_collection('seeds').update |
| Sequences | DELETE | `/api/v1/sequences/{id}` | 🟡 | biocollections.for_collection('sequences').delete |
| Sequences | GET | `/api/v1/sequences` | 🟡 | biocollections.for_collection('sequences').list |
| Sequences | GET | `/api/v1/sequences/{id}` | 🟡 | biocollections.for_collection('sequences').get |
| Sequences | POST | `/api/v1/sequences` | 🟡 | biocollections.for_collection('sequences').create |
| Sequences | PUT | `/api/v1/sequences/{id}` | 🟡 | biocollections.for_collection('sequences').update |
| Shopping list | DELETE | `/api/v1/shopping_list/{id}` | ❌ | no namespace |
| Shopping list | GET | `/api/v1/shopping_list` | ❌ | no namespace |
| Shopping list | GET | `/api/v1/shopping_list/{id}` | ❌ | no namespace |
| Shopping list | POST | `/api/v1/shopping_list/add_item` | ❌ | no namespace |
| Shopping list | PUT | `/api/v1/shopping_list/{id}` | ❌ | no namespace |
| Shopping list | PUT | `/api/v1/shopping_list/{id}/approve` | ❌ | no namespace |
| Shopping list | PUT | `/api/v1/shopping_list/{id}/cancel` | ❌ | no namespace |
| Shopping list | PUT | `/api/v1/shopping_list/{id}/submit` | ❌ | no namespace |
| Signature flows | DELETE | `/api/v1/signature_flows/{id}` | ❌ | no namespace |
| Stocks | DELETE | `/api/v1/stocks/{id}` | ✅ | stocks.delete |
| Stocks | GET | `/api/v1/stocks` | ✅ | stocks.list |
| Stocks | GET | `/api/v1/stocks/get_stocks_by_barcode` | ❌ | sub-action on stocks (client only) |
| Stocks | GET | `/api/v1/stocks/{id}` | ✅ | stocks.get |
| Stocks | POST | `/api/v1/stocks` | ✅ | stocks.create |
| Stocks | POST | `/api/v1/stocks/{id}/mark_as_consumed` | ❌ | sub-action on stocks (client only) |
| Stocks | POST | `/api/v1/stocks/{id}/mark_as_output` | ❌ | sub-action on stocks (client only) |
| Stocks | POST | `/api/v1/stocks/{id}/unmark_output` | ❌ | sub-action on stocks (client only) |
| Stocks | POST | `/api/v1/stocks/{id}/update_stock_amount` | ❌ | sub-action on stocks (client only) |
| Stocks | PUT | `/api/v1/stocks/{id}` | ✅ | stocks.update |
| Storages | DELETE | `/api/v1/storages/{id}` | ✅ | storages.delete |
| Storages | GET | `/api/v1/storages` | ✅ | storages.list |
| Storages | GET | `/api/v1/storages/{id}` | ✅ | storages.get |
| Storages | POST | `/api/v1/storages` | ✅ | storages.create |
| Storages | PUT | `/api/v1/storages/{id}` | ✅ | storages.update |
| Submodules | GET | `/api/v1/biocollections/{parent_collection_name}/get_derived_collections` | ❌ | no namespace |
| Submodules | GET | `/api/v1/biocollections/{parent_collection_name}/{id}/get_derived_items` | ❌ | no namespace |
| Submodules | GET | `/api/v1/{biocollection_name}/{id}/get_parents` | ❌ | no namespace |
| Submodules | GET | `/api/v1/{parent_collection_name}/get_derived_collections` | ❌ | no namespace |
| Submodules | GET | `/api/v1/{parent_collection_name}/{id}/get_derived_items` | ❌ | no namespace |
| Submodules | POST | `/api/v1/{biocollection_name}` | ❌ | no namespace |
| Submodules | PUT | `/api/v1/{biocollection_name}/{id}` | ❌ | no namespace |
| Tags | DELETE | `/api/v1/tags` | ❌ | sub-action on tags (client only) |
| Tags | DELETE | `/api/v1/tags/{id}` | ✅ | tags.delete |
| Tags | POST | `/api/v1/tags` | ✅ | tags.create |
| Teams | DELETE | `/api/v1/teams/{id}` | ❌ | no namespace |
| Teams | GET | `/api/v1/teams` | ❌ | no namespace |
| Teams | GET | `/api/v1/teams/{id}` | ❌ | no namespace |
| Tissue | DELETE | `/api/v1/tissues/{id}` | 🟡 | biocollections.for_collection('tissues').delete |
| Tissue | GET | `/api/v1/tissues` | 🟡 | biocollections.for_collection('tissues').list |
| Tissue | GET | `/api/v1/tissues/{id}` | 🟡 | biocollections.for_collection('tissues').get |
| Tissue | POST | `/api/v1/tissues` | 🟡 | biocollections.for_collection('tissues').create |
| Tissue | PUT | `/api/v1/tissues/{id}` | 🟡 | biocollections.for_collection('tissues').update |
| Units | DELETE | `/api/v1/units/{id}` | ✅ | units.delete |
| Units | GET | `/api/v1/units` | ✅ | units.list |
| Units | GET | `/api/v1/units/{id}` | ✅ | units.get |
| Units | POST | `/api/v1/units` | ✅ | units.create |
| Vectors | DELETE | `/api/v1/vectors/{id}` | ❌ | no namespace |
| Vectors | GET | `/api/v1/vectors` | ❌ | no namespace |
| Vectors | GET | `/api/v1/vectors/{id}` | ❌ | no namespace |
| Vectors | POST | `/api/v1/vectors` | ❌ | no namespace |
| Vectors | PUT | `/api/v1/vectors/{id}` | ❌ | no namespace |
| Viruses | DELETE | `/api/v1/viruses/{id}` | 🟡 | biocollections.for_collection('viruses').delete |
| Viruses | GET | `/api/v1/viruses` | 🟡 | biocollections.for_collection('viruses').list |
| Viruses | GET | `/api/v1/viruses/{id}` | 🟡 | biocollections.for_collection('viruses').get |
| Viruses | POST | `/api/v1/viruses` | 🟡 | biocollections.for_collection('viruses').create |
| Viruses | PUT | `/api/v1/viruses/{id}` | 🟡 | biocollections.for_collection('viruses').update |
| Visualizations | DELETE | `/api/v1/visualizations/{id}` | ✅ | visualizations.delete |
| Visualizations | POST | `/api/v1/visualizations` | ✅ | visualizations.create |
| Webhooks | DELETE | `/api/v1/webhooks/{id}` | ✅ | webhooks.delete |
| Webhooks | GET | `/api/v1/webhooks` | ✅ | webhooks.list |
| Webhooks | GET | `/api/v1/webhooks/list` | ❌ | sub-action on webhooks (client only) |
| Webhooks | GET | `/api/v1/webhooks/{id}` | ✅ | webhooks.get |
| Webhooks | POST | `/api/v1/webhooks` | ✅ | webhooks.create |
| Webhooks | PUT | `/api/v1/webhooks/{id}` | ✅ | webhooks.update |
| Workflows | DELETE | `/api/v1/workflows/{id}` | 🚫 | workflows.delete raises LabguruError |
| Workflows | GET | `/api/v1/workflows` | ✅ | workflows.list |
| Workflows | GET | `/api/v1/workflows/{id}` | ✅ | workflows.get |
| Worms | DELETE | `/api/v1/worms/{id}` | 🟡 | biocollections.for_collection('worms').delete |
| Worms | GET | `/api/v1/worms` | 🟡 | biocollections.for_collection('worms').list |
| Worms | GET | `/api/v1/worms/{id}` | 🟡 | biocollections.for_collection('worms').get |
| Worms | POST | `/api/v1/worms` | 🟡 | biocollections.for_collection('worms').create |
| Worms | PUT | `/api/v1/worms/{id}` | 🟡 | biocollections.for_collection('worms').update |
| Yeasts | DELETE | `/api/v1/yeasts/{id}` | 🟡 | biocollections.for_collection('yeasts').delete |
| Yeasts | GET | `/api/v1/yeasts` | 🟡 | biocollections.for_collection('yeasts').list |
| Yeasts | GET | `/api/v1/yeasts/{id}` | 🟡 | biocollections.for_collection('yeasts').get |
| Yeasts | POST | `/api/v1/yeasts` | 🟡 | biocollections.for_collection('yeasts').create |
| Yeasts | PUT | `/api/v1/yeasts/{id}` | 🟡 | biocollections.for_collection('yeasts').update |
| Zebrafishes | DELETE | `/api/v1/zebrafishes/{id}` | 🟡 | biocollections.for_collection('zebrafishes').delete |
