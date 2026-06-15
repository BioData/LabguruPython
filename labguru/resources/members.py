# labguru/resources/members.py
from labguru.resources.base import BaseResource
from labguru.exceptions import LabguruError


class MembersResource(BaseResource):
    """Read-only: the Labguru members API exposes index/show only."""

    resource_name = "members"

    def create(self, *args, **kwargs):
        raise LabguruError("members is read-only; create is not supported")

    def update(self, *args, **kwargs):
        raise LabguruError("members is read-only; update is not supported")

    def delete(self, *args, **kwargs):
        raise LabguruError("members is read-only; delete is not supported")
