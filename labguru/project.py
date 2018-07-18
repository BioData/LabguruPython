# -*- coding: utf-8 -*-
from __future__ import print_function
from requests import HTTPError
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


class Project(object):
    def __init__(self, title, id=None, description=None, *args, **kwargs):
        self.title = title
        self.id = id
        self.description = description
        # self.orders = orders

    def __str__(self):
        return json.dumps(self.__dict__)

    def create_new_folder(self, token, description=None):
        url = api.normalise('/api/v1/milestones.json')
        data = {
            'token': token,
            'item': {
                "project_id": self.id,
                "owner_id": 1,
                "title": self.title,
                "description": "dddddd"
            }
        }
        return api.request(url, data=data)
