# -*- coding: utf-8 -*-
from __future__ import print_function
from requests import HTTPError
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
            raise UnAuthorizeException('Login failed! Wrong email or password')
        else:
            self.session = Session(**response)

    def create_new_project(self, title, description=None):
        url = api.normalise('/api/v1/projects.json')
        item = Project(title, description)

        assert isinstance(title, str) and len(title) > 0, 'title is required to create a new project'

        data = {
            'token': self.session.token,
            'item': item.__dict__
        }
        try:
            response = api.request(url, data=data)
            return Project(**response)
        except HTTPError:
            raise DuplicatedException('Duplicated title: {title} in the lab'.format(title=title))

    def get_project(self, project_id):
        url = api.normalise('/api/v1/projects/{id}.json'.format(id=project_id))
        params = {
            'token': self.session.token
        }
        try:
            response = api.request(url, method='GET', data=params)
            return Project(**response)
        except HTTPError:
            raise NotFoundException('Project {id} does not exist'.format(id=project_id))

    def get_all_projects(self, page_num):
        url = api.normalise('/api/v1/projects.json')
        params = {
            'token': self.session.token,
            'page': page_num
        }
        response = api.request(url, method='GET', data=params)
        if isinstance(response, list):
            return [Project(**item) for item in response]
        else:
            return []


class Session(object):
    def __init__(self, token, url, admin, orders, *args, **kwargs):
        self.token = token
        self.url = url
        self.admin = admin
        self.orders = orders

    def __str__(self):
        return json.dumps(self.__dict__)


class UnAuthorizeException(Exception):
    pass


class NotFoundException(Exception):
    pass


class DuplicatedException(Exception):
    pass