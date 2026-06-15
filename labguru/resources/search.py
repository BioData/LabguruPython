# labguru/resources/search.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class SearchResource(BaseResource):
    """Read-only search endpoint; only global_search is supported."""

    resource_name = "searches"

    def global_search(self, term: str, **params):
        params["term"] = term
        return self.client.get(self._path("/global_search"), params=params)

    def create(self, *args, **kwargs):
        raise LabguruError("searches is read-only; create is not supported")

    def update(self, *args, **kwargs):
        raise LabguruError("searches is read-only; update is not supported")

    def delete(self, *args, **kwargs):
        raise LabguruError("searches is read-only; delete is not supported")
