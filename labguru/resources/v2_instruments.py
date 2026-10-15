# labguru/resources/v2_instruments.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class InstrumentsV2Resource(BaseResource):
    """API v2 equipment: list only, with ``page`` / ``page_size`` paging."""

    resource_name = "instruments"
    api_version = "v2"

    def get(self, *args, **kwargs):
        raise LabguruError("v2 instruments supports list only")

    def create(self, *args, **kwargs):
        raise LabguruError("v2 instruments supports list only")

    def update(self, *args, **kwargs):
        raise LabguruError("v2 instruments supports list only")

    def delete(self, *args, **kwargs):
        raise LabguruError("v2 instruments supports list only")
