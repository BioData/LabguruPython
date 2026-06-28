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
