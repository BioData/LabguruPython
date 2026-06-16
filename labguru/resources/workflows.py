# labguru/resources/workflows.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class WorkflowsResource(BaseResource):
    """Read-only. The API exposes GET index and show only — no create/update/delete."""

    resource_name = "workflows"

    def create(self, *args, **kwargs):
        raise LabguruError("workflows is read-only; create is not supported")

    def update(self, *args, **kwargs):
        raise LabguruError("workflows is read-only; update is not supported")

    def delete(self, *args, **kwargs):
        raise LabguruError("workflows is read-only; delete is not supported")
