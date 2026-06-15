# labguru/facade.py
from __future__ import annotations

from typing import Optional

from labguru.client import LabguruClient
from labguru.exceptions import LabguruError
from labguru.resources.biocollections import BiocollectionsResource
from labguru.resources.elements import ElementsResource
from labguru.resources.experiments import ExperimentsResource
from labguru.resources.members import MembersResource
from labguru.resources.projects import ProjectsResource
from labguru.resources.protocols import ProtocolsResource
from labguru.resources.search import SearchResource
from labguru.resources.sections import SectionsResource
from labguru.resources.stocks import StocksResource
from labguru.resources.storages import StoragesResource
from labguru.resources.tags import TagsResource


class Labguru:
    """Entry point. Usage: `lab = Labguru(url="https://my.labguru.com", token="...")`."""

    def __init__(self, url: Optional[str] = None, token: Optional[str] = None, **legacy):
        if token is None or url is None:
            if "login" in legacy or "password" in legacy:
                raise LabguruError(
                    "Email/password auth was removed in 2.0. Pass an API token: "
                    "Labguru(url='https://my.labguru.com', token='...'). "
                    "Get a token from your Labguru account settings."
                )
            raise LabguruError("Labguru(url=..., token=...) are required.")
        self.client = LabguruClient(url, token)
        self.protocols = ProtocolsResource(self.client)
        self.experiments = ExperimentsResource(self.client)
        self.sections = SectionsResource(self.client)
        self.elements = ElementsResource(self.client)
        self.members = MembersResource(self.client)
        self.tags = TagsResource(self.client)
        self.search = SearchResource(self.client)
        self.biocollections = BiocollectionsResource(self.client)
        self.stocks = StocksResource(self.client)
        self.storages = StoragesResource(self.client)
        self.projects = ProjectsResource(self.client)
