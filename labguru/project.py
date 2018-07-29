# -*- coding: utf-8 -*-
from __future__ import print_function
from requests import HTTPError
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
    def __init__(self, token=None, id=None, title=None, **kwargs):
        Response.__init__(self, token, **kwargs)
        self.title = title
        self.id = id
        # self.description = description
        # self.milestones = milestones
        self.endpoint = '/api/v1/projects.json'
        self.specific_endpoint = '/api/v1/projects/{id}.json'

    def register(self):
        response = self._add(endpoint=self.endpoint, item=self.to_dict())
        return self.__class__(token=self.token, **response)

    def get(self):
        response = self._get_or_update(endpoint=self.specific_endpoint, id=self.id, method='GET')
        return self.__class__(token=self.token, **response)

    def list(self, name=None, page_num=None):

        response = self.find(endpoint=self.endpoint, name=name, page_num=page_num)
        if isinstance(response, list):
            return [self.__class__(token=self.token, **item) for item in response]
        else:
            return []

    def update(self):
        response = self._get_or_update(endpoint=self.specific_endpoint, id=self.id, method='PUT', item=self.to_dict())
        return self.__class__(token=self.token, **response)

    # def milestones(self):
    #     if self.milestones:
    #         return [Folder(project_id=self.id, token=self.token, **milestone) for milestone in self.milestones]
    #     else:
    #         return []

    # def add_folder(self, title, description=None, **kwargs):
    #     response = self._add(endpoint='/api/v1/milestones.json',
    #                          project_id=self.id,
    #                          title=title,
    #                          description=description, **kwargs)
    #     return Folder(token=self.token, **response)
    #
    # def get_folder(self, folder_id):
    #     response = self._get_or_update(endpoint='/api/v1/milestones/{id}.json', id=folder_id, method='GET')
    #     return Folder(token=self.token, project_id=self.id, **response)
    #
    # def __get_folders(self, period=None, page_num=None):
    #     response = self.find(endpoint='/api/v1/milestones.json',
    #                          project_id=self.id,
    #                          period=period,
    #                          page_num=page_num)
    #     if isinstance(response, list) and len(response) > 0:
    #         return [Folder(project_id=self.id, token=self.token, **item) for item in response]
    #     else:
    #         return []
    #
    # def list_folders(self, page_num):
    #     return self.__get_folders(page_num=page_num)
    #
    # def get_current_folders(self):
    #     return self.__get_folders(period='current_milestones')
    #
    # def get_future_folders(self):
    #     return self.__get_folders(period='future_milestones')
    #
    # def get_past_folders(self):
    #     return self.__get_folders(period='last_milestones')
