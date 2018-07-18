# -*- coding: utf-8 -*-
from __future__ import print_function
import json

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

    def __init__(self, title, description=None, id=None, *args, **kwargs):
        self.id = id
        self.title = title
        self.description = description
        # self.orders = orders

    def __str__(self):
        return json.dumps(self.__dict__)
