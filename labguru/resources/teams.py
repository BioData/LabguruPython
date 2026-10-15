# labguru/resources/teams.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class TeamsResource(BaseResource):
    """Teams: list, get and delete (no create/update endpoint)."""

    resource_name = "teams"

    def create(self, *args, **kwargs):
        raise LabguruError("teams supports list, get and delete only; create is not available")

    def update(self, *args, **kwargs):
        raise LabguruError("teams supports list, get and delete only; update is not available")
