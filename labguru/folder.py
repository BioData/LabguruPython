# -*- coding: utf-8 -*-
from __future__ import print_function

from project import Project


class Folder(Project):
    def __init__(self, token=None, id=None, title=None, project_id=None, **kwargs):
        Project.__init__(self, token, id, title, **kwargs)
        self.project_id = project_id
        self.endpoint = '/api/v1/milestones.json'
        self.specific_endpoint = '/api/v1/milestones/{id}.json'

    def __get_folders(self, period=None):
        response = self.find(endpoint=self.endpoint, project_id=self.id, period=period)
        if isinstance(response, list) and len(response) > 0:
            return [Folder(project_id=self.id, token=self.token, **item) for item in response]
        else:
            return []

    def get_current_folders(self):
        return self.__get_folders(period='current_milestones')

    def get_future_folders(self):
        return self.__get_folders(period='future_milestones')

    def get_past_folders(self):
        return self.__get_folders(period='last_milestones')

    # def add_experiment(self, title, description=None, step=None, **kwargs):
    #     response = self._add(endpoint='/api/v1/experiments.json',
    #                          project_id=self.project_id,
    #                          milestone_id=self.id,
    #                          title=title,
    #                          description=description,
    #                          step=step, **kwargs)
    #
    #     return Experiment(token=self.token, project_id=self.project_id, milestone_id=self.id, **response)
