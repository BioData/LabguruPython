# labguru/v2.py
"""Namespaces for endpoints that exist only under ``/api/v2`` (``lab.v2.<name>``)."""
from labguru.resources.v2_experiments import ExperimentsV2Resource
from labguru.resources.v2_reports import ReportsV2Resource


class LabguruV2:
    def __init__(self, client):
        self.experiments = ExperimentsV2Resource(client)
        self.reports = ReportsV2Resource(client)
