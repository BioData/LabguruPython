# labguru/resources/workflows.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class WorkflowsResource(BaseResource):
    """List, get and delete. The API has no create/update endpoint."""

    resource_name = "workflows"

    def create(self, *args, **kwargs):
        raise LabguruError("workflows has no create endpoint; create is not supported")

    def update(self, *args, **kwargs):
        raise LabguruError("workflows has no update endpoint; update is not supported")
