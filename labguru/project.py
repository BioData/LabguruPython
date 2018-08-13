# -*- coding: utf-8 -*-
from __future__ import print_function
from .response import Response


# Level 1
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


# Level 2
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


# Level 2.1
class Experiment(Project):
    def __init__(self, token=None, project_id=None, milestone_id=None, id=None, title=None, **kwargs):
        Project.__init__(self, token, id, title, **kwargs)
        self.project_id = project_id
        self.milestone_id = milestone_id
        self.endpoint = '/api/v1/experiments.json'
        self.specific_endpoint = '/api/v1/experiments/{id}.json'


# Level 2.2
class Procedure(Project):
    def __init__(self, token=None, container_id=None, id=None, name=None, section_type=None, container_type=None,
                 **kwargs):
        Project.__init__(self, token, id, **kwargs)
        self.container_id = container_id
        self.name = name
        self.section_type = section_type
        self.container_type = container_type
        self.endpoint = '/api/v1/element_containers.json'
        self.specific_endpoint = '/api/v1/element_containers/{id}.json'


# Level 2.3
class Element(Project):
    def __init__(self, token=None, container_id=None, id=None, data=None, element_type=None, container_type=None,
                 **kwargs):
        Project.__init__(self, token, id, **kwargs)
        self.container_id = container_id
        self.data = data
        self.element_type = element_type
        self.container_type = container_type
        self.endpoint = '/api/v1/elements.json'
        self.specific_endpoint = '/api/v1/elements/{id}.json'
