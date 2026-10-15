# labguru/resources/biocollections.py
from labguru.resources.base import BaseResource


class BiocollectionsResource(BaseResource):
    item_key = "item"

    def __init__(self, client, collection: str = "plasmids"):
        super().__init__(client)
        if not collection:
            raise ValueError("collection must be a non-empty string")
        self.resource_name = collection

    def for_collection(self, collection: str) -> "BiocollectionsResource":
        """Address a built-in collection at its direct path, e.g.
        ``for_collection("plasmids")`` -> ``/api/v1/plasmids``.
        """
        return BiocollectionsResource(self.client, collection)

    def for_generic_collection(self, collection: str) -> "BiocollectionsResource":
        """Address a custom/generic collection via the ``biocollections/`` prefix,
        e.g. ``for_generic_collection("my_assays")`` ->
        ``/api/v1/biocollections/my_assays`` (GET/POST, and PUT/GET on ``/{id}``).
        This is the 2.0 equivalent of the 1.x generic-inventory-item API.
        """
        return BiocollectionsResource(self.client, f"biocollections/{collection}")

    def create(self, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.post(self._path(), {self.item_key: fields})

    def update(self, resource_id, fields: dict):
        """fields: inner payload, wrapped as {item_key: fields} before sending."""
        return self.client.put(self._path(f"/{resource_id}"), {self.item_key: fields})

    def find_by_external_uuid(self, external_uuid: str):
        """Look up items by external_uuid.

        WARNING: `external_uuid` is not a documented query parameter in the
        Labguru API spec (OpenAPI v1) — the collection index only documents
        `page`/`meta`, and server-side filtering goes through the Kendo
        `/api/v1/{collection_name}` filter endpoint. This sends a plain
        `?external_uuid=` and is UNVERIFIED — see the ledger in MIGRATION.md.
        """
        return self.client.get(self._path(), params={"external_uuid": external_uuid})

    def parents(self, resource_id):
        """Parent items of an inventory item (GET /{collection}/{id}/get_parents)."""
        return self.client.get(self._path(f"/{resource_id}/get_parents"))

    def derived_collections(self):
        """Collections derived from this one (GET /{collection}/get_derived_collections)."""
        return self.client.get(self._path("/get_derived_collections"))

    def derived_items(self, resource_id, derived_collection_name=None,
                      derived_collection_id=None):
        """Items derived from this item, in one derived collection given by name or id."""
        if not (derived_collection_name or derived_collection_id):
            raise ValueError("pass derived_collection_name or derived_collection_id")
        params = {}
        if derived_collection_name:
            params["derived_collection_name"] = derived_collection_name
        if derived_collection_id:
            params["derived_collection_id"] = derived_collection_id
        return self.client.get(self._path(f"/{resource_id}/get_derived_items"), params=params)
