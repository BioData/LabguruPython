# -*- coding: utf-8 -*-
from __future__ import print_function

import json

from requests import HTTPError

import api
from exception import UnAuthorizeException, NotFoundException, DuplicatedException
from project import Project
from folder import Folder


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

    def __project_api(self, endpoint='/api/v1/projects.json', method='GET', *args, **kwargs):
        return api.call(token=self.session.token, endpoint=endpoint, method=method, data=kwargs)

    def add_project(self, title, description=None):
        assert isinstance(title, str) and len(title) > 0, 'title is required to create a new project'

        item = Project(title=title, description=description)
        response = self.__project_api(method='POST', item=item.to_dict())
        return Project(**response)

    def get_project(self, project_id):
        endpoint = '/api/v1/projects/{id}.json'.format(id=project_id)
        try:
            response = self.__project_api(endpoint, method='GET', id=project_id)
            return Project(token=self.session.token, **response)
        except HTTPError:
            raise NotFoundException('Project {id} does not exist'.format(id=project_id))

    def find_project(self, name):
        response = self.__project_api(name=name)
        if isinstance(response, list):
            return [Project(token=self.session.token, **item) for item in response]
        else:
            return []

    def update_project(self, project_id, title, description=None):
        endpoint = '/api/v1/projects/{id}.json'.format(id=project_id)
        item = Project(title=title, description=description)
        try:
            response = self.__project_api(endpoint, method='PUT', item=item.to_dict())
            return Project(token=self.session.token, **response)
        except HTTPError:
            raise NotFoundException('Project {id} does not exist'.format(id=project_id))

    def archive_project(self):
        pass

    def list_projects(self, page_num):
        response = self.__project_api(page=page_num)
        if isinstance(response, list):
            return [Project(token=self.session.token, **item) for item in response]
        else:
            return []

    def get_folder(self, folder_id):
        url = api.normalise('/api/v1/milestones/{id}.json'.format(id=folder_id))
        params = {
            'token': self.session.token
        }
        try:
            response = api.request(url, method='GET', data=params)
            return Folder(token=self.session.token, **response)
        except HTTPError:
            raise NotFoundException('Folder {id} does not exist'.format(id=folder_id))

    def list_folders(self, page_num):
        url = api.normalise('/api/v1/milestones.json')
        params = {
            'token': self.session.token,
            'page': page_num
        }
        response = api.request(url, method='GET', data=params)
        if isinstance(response, list):
            return [Folder(token=self.session.token, **item) for item in response]
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
