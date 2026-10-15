# labguru/v2.py
"""Namespaces for endpoints that exist only under ``/api/v2`` (``lab.v2.<name>``)."""
from labguru.resources.v2_experiments import ExperimentsV2Resource
from labguru.resources.v2_instruments import InstrumentsV2Resource
from labguru.resources.v2_reports import ReportsV2Resource
from labguru.resources.v2_rodent_cages import RodentCagesV2Resource


class LabguruV2:
    def __init__(self, client):
        self.experiments = ExperimentsV2Resource(client)
        self.reports = ReportsV2Resource(client)
        self.instruments = InstrumentsV2Resource(client)
        self.rodent_cages = RodentCagesV2Resource(client)
