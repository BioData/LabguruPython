# labguru/resources/forms.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class FormsResource(BaseResource):
    """Forms: delete only (the only documented endpoint)."""

    resource_name = "forms"

    def list(self, *args, **kwargs):
        raise LabguruError("forms supports delete only; list is not available")

    def get(self, *args, **kwargs):
        raise LabguruError("forms supports delete only; get is not available")

    def create(self, *args, **kwargs):
        raise LabguruError("forms supports delete only; create is not available")

    def update(self, *args, **kwargs):
        raise LabguruError("forms supports delete only; update is not available")
