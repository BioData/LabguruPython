# labguru/resources/signature_flows.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class SignatureFlowsResource(BaseResource):
    """Signature flows: delete only (the only documented endpoint)."""

    resource_name = "signature_flows"

    def list(self, *args, **kwargs):
        raise LabguruError("signature_flows supports delete only; list is not available")

    def get(self, *args, **kwargs):
        raise LabguruError("signature_flows supports delete only; get is not available")

    def create(self, *args, **kwargs):
        raise LabguruError("signature_flows supports delete only; create is not available")

    def update(self, *args, **kwargs):
        raise LabguruError("signature_flows supports delete only; update is not available")
