# labguru/resources/members.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class MembersResource(BaseResource):
    """Read-only: the Labguru members API exposes index/show only."""

    resource_name = "members"

    def create(self, *args, **kwargs):
        raise LabguruError("members is read-only; create is not supported")

    def update(self, *args, **kwargs):
        raise LabguruError("members is read-only; update is not supported")

    def delete(self, *args, **kwargs):
        raise LabguruError("members is read-only; delete is not supported")
