# labguru/resources/search.py
from labguru.resources.base import BaseResource


class SearchResource(BaseResource):
    resource_name = "searches"

    def global_search(self, term: str, **params):
        params["term"] = term
        return self.client.get("/api/v1/searches/global_search", params=params)
