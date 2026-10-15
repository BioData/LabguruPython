# labguru/resources/v2_rodent_cages.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class RodentCagesV2Resource(BaseResource):
    """API v2 rodent cages: list only, with ``page`` / ``page_size`` paging."""

    resource_name = "rodent_cages"
    api_version = "v2"

    def get(self, *args, **kwargs):
        raise LabguruError("v2 rodent_cages supports list only")

    def create(self, *args, **kwargs):
        raise LabguruError("v2 rodent_cages supports list only")

    def update(self, *args, **kwargs):
        raise LabguruError("v2 rodent_cages supports list only")

    def delete(self, *args, **kwargs):
        raise LabguruError("v2 rodent_cages supports list only")
