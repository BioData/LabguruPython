# -*- coding: utf-8 -*-
from __future__ import print_function
from requests import HTTPError
from folder import Folder
from pojo import Response
from exception import *
import json
import api


# {
# "id": 101,
# "uuid": "f6ddee4d-1ea7-47f2-9519-ea6a377ed151",
# "title": "FtsH function in Chloroplasts",
# "user": 371,
# "description": "one of the first widely used E. coli cloning vectors.",
# "created_at": "2018-07-17",
# "owner_id": 31,
# "milestones": [],
# "comments": [],
# "experiment_procedures": [],
# "attachments": [],
# "archived": false,
# "api_url": "/api/v1/projects/101",
# "viewers": [],
# "owner": {...}
# }


class Project(Response):
    def __init__(self, token=None, id=None, title=None, description=None, milestones=None, **kwargs):
        Response.__init__(self, token, **kwargs)
        self.title = title
        self.id = id
        self.description = description
        self.milestones = milestones

    def add_folder(self, title, description=None, **kwargs):
        response = self._add(endpoint='/api/v1/milestones.json',
                             project_id=self.id,
                             title=title,
                             description=description, **kwargs)
        return Folder(token=self.token, **response)

    def list_folders(self):
        if self.milestones:
            return [Folder(project_id=self.id, token=self.token, **milestone) for milestone in self.milestones]
        else:
            return []

    def __get_folders(self, period):
        url = api.normalise('/api/v1/milestones.json')
        params = {
            'token': self.token,
            'project_id': self.id,
            'period': period
        }
        response = api.request(url, method='GET', data=params)
        if isinstance(response, list) and len(response) > 0:
            return [Folder(project_id=self.id, token=self.token, **item) for item in response]
        else:
            return []

    def get_current_folders(self):
        return self.__get_folders('current_milestones')

    def get_future_folders(self):
        return self.__get_folders('future_milestones')

    def get_past_folders(self):
        return self.__get_folders('last_milestones')
