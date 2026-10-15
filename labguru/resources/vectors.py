# labguru/resources/vectors.py
from labguru.resources.base import BaseResource


class VectorsResource(BaseResource):
    """Dataset vectors (not the `vectors` biocollection). Full CRUD; the body is
    top-level ``{dataset_id, vector_data}``, not wrapped under ``item``."""

    resource_name = "vectors"

    def create(self, dataset_id, vector_data: str):
        return self.client.post(
            self._path(), {"dataset_id": dataset_id, "vector_data": vector_data}
        )

    def update(self, resource_id, dataset_id=None, vector_data=None):
        body = {k: v for k, v in (("dataset_id", dataset_id), ("vector_data", vector_data))
                if v is not None}
        return self.client.put(self._path(f"/{resource_id}"), body)
