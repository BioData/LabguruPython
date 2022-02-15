# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
from datetime import datetime
import json

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
        self.endpoint = '/api/v1/sections.json'
        self.specific_endpoint = '/api/v1/sections/{id}.json'


# Level 2.3
class Element(Project):
    def __init__(self, token=None, container_id=None, id=None, data=None, element_type=None, container_type=None,
                 experiment_id=None, **kwargs):
        Project.__init__(self, token, id, **kwargs)
        self.experiment_id = experiment_id
        self.container_id = container_id
        self.data = data
        self.element_type = element_type
        self.container_type = container_type
        self.endpoint = '/api/v1/elements.json'
        self.specific_endpoint = '/api/v1/elements/{id}.json'
        self.specific_endpoint_type = '/api/v1/experiments/{id}/elements.json'
        self.update_stock_amount_endpoint = '/api/v1/stocks/{id}/update_stock_amount'
        self.add_attachment_endpoint = '/api/v1/attachments/{id}'

    def update_element(self):
        response = self._get_or_update(endpoint=self.specific_endpoint, id=self.id, method='PUT', element=self.to_dict())
        return self.__class__(token=self.token, **response)

    def list_by_type(self):
        response = self._get_or_update(endpoint=self.specific_endpoint_type, id=self.experiment_id,
                                       element_type=self.element_type)
        if isinstance(response, list):
            return [self.__class__(token=self.token, **item) for item in response]
        else:
            return []

    def get_data(self):
        if self.element_type == 'form':
            return json.loads(self.description).get('form_json')

        elif self.element_type == 'samples':
            return json.loads(self.data).get('samples')

        elif self.element_type == 'plate':
            return json.loads(self.data).get('wells')

        else:
            return self.data


    def update_stock_amount(self, sample_id, stock_id, amount_used, unit_type, unit_type_name):
        if self.element_type == 'samples':
            response = self._get_or_update(endpoint=self.update_stock_amount_endpoint,
                                           id=stock_id,
                                           amount_used=amount_used,
                                           unit_type=unit_type,
                                           unit_type_name=unit_type_name,
                                           element_id=self.id,
                                           sample_id=sample_id,
                                           subtract='true',
                                           method='POST')
            return self.__class__(token=self.token, **response)
        else:
            return []

    def add_step(self, txt='', hours='00', minutes='00', seconds='00', completed_by=''):
        if self.element_type == 'steps':
            step = {
                "title": '<p>' + txt + '</p>',
                "timer": {
                    "hours": hours,
                    "minutes": minutes,
                    "seconds": seconds
                },
                "completed": True,
                "completed_by": completed_by,
                "completed_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }

            steps = json.loads(self.data)
            steps.append(step)
            data = json.dumps(steps)
            response = self._get_or_update(endpoint=self.specific_endpoint, id=self.id, method='PUT', data=data)
            return self.__class__(token=self.token, **response)
        else:
            return []

    def add_attachment(self, attachment_id):
        if self.element_type == 'attachments':
            response = self._get_or_update(endpoint=self.add_attachment_endpoint,
                                           id=attachment_id,
                                           item={'element_id': self.id},
                                           method='PUT')
            return self.__class__(token=self.token, **response)
        else:
            return []
