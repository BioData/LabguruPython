# -*- coding: utf-8 -*-
from __future__ import print_function
from requests import HTTPError
from pojo import Response
from experiment import Experiment
import json
import api


class Folder(Response):
    def __init__(self, token=None, id=None, title=None, project_id=None, description=None, milestones=None, **kwargs):
        Response.__init__(self, token, **kwargs)
        self.project_id = project_id
        self.title = title
        self.id = id
        self.description = description
        self.milestones = milestones

    def add_experiment(self, title, description=None, step=None, **kwargs):
        response = self._add(endpoint='/api/v1/experiments.json',
                             project_id=self.project_id,
                             milestone_id=self.id,
                             title=title,
                             description=description,
                             step=step, **kwargs)

        return Experiment(token=self.token, project_id=self.project_id, milestone_id=self.id, **response)
