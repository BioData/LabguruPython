# labguru/facade.py
from __future__ import annotations

from typing import Optional

from labguru.client import LabguruClient
from labguru.exceptions import LabguruError
from labguru.resources.attachments import AttachmentsResource
from labguru.resources.biocollections import BiocollectionsResource
from labguru.resources.boxes import BoxesResource
from labguru.resources.comments import CommentsResource
from labguru.resources.datasets import DatasetsResource
from labguru.resources.documents import DocumentsResource
from labguru.resources.elements import ElementsResource
from labguru.resources.experiments import ExperimentsResource
from labguru.resources.instruments import InstrumentsResource
from labguru.resources.measurements import MeasurementsResource
from labguru.resources.members import MembersResource
from labguru.resources.notes import NotesResource
from labguru.resources.papers import PapersResource
from labguru.resources.projects import ProjectsResource
from labguru.resources.protocols import ProtocolsResource
from labguru.resources.reports import ReportsResource
from labguru.resources.requests import RequestsResource
from labguru.resources.search import SearchResource
from labguru.resources.sections import SectionsResource
from labguru.resources.sops import SopsResource
from labguru.resources.stocks import StocksResource
from labguru.resources.storages import StoragesResource
from labguru.resources.tags import TagsResource
from labguru.resources.units import UnitsResource
from labguru.resources.visualizations import VisualizationsResource
from labguru.resources.webhooks import WebhooksResource
from labguru.resources.workflows import WorkflowsResource


class Labguru:
    """Entry point. Usage: `lab = Labguru(url="https://my.labguru.com", token="...")`."""

    def __init__(self, url: Optional[str] = None, token: Optional[str] = None, **legacy):
        if "login" in legacy or "password" in legacy:
            raise LabguruError(
                "Email/password auth was removed in 2.0. Pass an API token: "
                "Labguru(url='https://my.labguru.com', token='...'). "
                "Get a token from your Labguru account settings."
            )
        if not token or not url:
            raise LabguruError("Labguru(url=..., token=...) are required.")
        self.client = LabguruClient(url, token)
        # Experiment / knowledge resources
        self.projects = ProjectsResource(self.client)
        self.experiments = ExperimentsResource(self.client)
        self.sections = SectionsResource(self.client)
        self.elements = ElementsResource(self.client)
        self.protocols = ProtocolsResource(self.client)
        self.datasets = DatasetsResource(self.client)
        self.documents = DocumentsResource(self.client)
        self.notes = NotesResource(self.client)
        self.papers = PapersResource(self.client)
        self.reports = ReportsResource(self.client)
        self.sops = SopsResource(self.client)
        self.workflows = WorkflowsResource(self.client)
        # Inventory / storage
        self.biocollections = BiocollectionsResource(self.client)
        self.stocks = StocksResource(self.client)
        self.storages = StoragesResource(self.client)
        self.boxes = BoxesResource(self.client)
        self.instruments = InstrumentsResource(self.client)
        self.units = UnitsResource(self.client)
        # Workflow / collaboration
        self.requests = RequestsResource(self.client)
        self.measurements = MeasurementsResource(self.client)
        self.visualizations = VisualizationsResource(self.client)
        self.webhooks = WebhooksResource(self.client)
        self.attachments = AttachmentsResource(self.client)
        self.comments = CommentsResource(self.client)
        self.tags = TagsResource(self.client)
        self.members = MembersResource(self.client)
        self.search = SearchResource(self.client)
