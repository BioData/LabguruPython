# -*- coding: utf-8 -*-
from __future__ import print_function
from requests import HTTPError
import json
import api


class Folder(object):
    def __init__(self, project_id, title, id=None, description=None, milestones=None, *args, **kwargs):
        self.project_id = project_id
        self.title = title
        self.id = id
        self.description = description
        self.milestones = milestones

    def __str__(self):
        return json.dumps(self.__dict__)