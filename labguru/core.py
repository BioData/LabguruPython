# -*- coding: utf-8 -*-
from __future__ import print_function
from project import Project
import api
import json


class Labguru(object):

    def __init__(self, login, password):
        data = {
            'login': login,
            'password': password
        }

        url = api.normalise('/api/v1/sessions.json')
        response = api.request(url, data=data)
        if response.get('token') == '-1':
            raise ValueError('Login failed! Wrong email or password')
        else:
            self.session = Session(**response)

    def get_project(self, project_id):
        url = api.normalise('/api/v1/projects/{id}.json'.format(id=project_id))
        params = {
            'token': self.session.token
        }
        response = api.request(url, method='GET', data=params)
        return Project(**response)


class Session(object):
    def __init__(self, token, url, admin, orders, *args, **kwargs):
        self.token = token
        self.url = url
        self.admin = admin
        self.orders = orders

    def __str__(self):
        return json.dumps(self.__dict__)
