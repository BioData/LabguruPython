# -*- coding: utf-8 -*-
from __future__ import print_function
from requests import HTTPError
import json
import api


class Folder(object):
    def __init__(self, title, id=None, project_id=None, description=None, milestones=None, token=None, *args, **kwargs):
        self.project_id = project_id
        self.title = title
        self.id = id
        self.description = description
        self.milestones = milestones
        self.token = token

    def __str__(self):
        return json.dumps(self.__dict__)