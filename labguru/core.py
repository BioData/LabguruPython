# -*- coding: utf-8 -*-
from __future__ import print_function

from . import api
from .error import UnAuthorizeException
from .project import Project, Folder, Experiment, Section, Element
from .response import Session


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

    """
    Project API
    """
    def add_project(self, title, description=None):
        assert isinstance(title, str) and len(title) > 0, 'title is required to create a new project'

        return Project(token=self.session.token, title=title, description=description).register()

    def get_project(self, project_id):
        proj = Project(id=project_id, token=self.session.token)
        return proj.get()

    def find_project(self, name):
        return Project(token=self.session.token).list(name=name)

    def update_project(self, project_id, title, description=None):
        proj = Project(token=self.session.token, id=project_id, title=title, description=description)
        return proj.update()

    def archive_project(self):
        pass

    def list_projects(self, page_num):
        return Project(token=self.session.token).list(page_num=page_num)

    """
    Folder API
    """
    def add_folder(self, project_id, title, description=None):
        return Folder(token=self.session.token, project_id=project_id, title=title, description=description).register()

    def get_folder(self, folder_id):
        return Folder(token=self.session.token, id=folder_id).get()

    def find_folder(self, name):
        return Folder(token=self.session.token).list(name=name)

    def update_folder(self, folder_id, title, description=None):
        return Folder(token=self.session.token, id=folder_id, title=title, description=description).update()

    def list_folders(self, project_id=None, page_num=None):
        if project_id is not None:
            milestones = self.get_project(project_id=project_id).milestones
            assert isinstance(milestones, list)
            return [Folder(token=self.session.token, project_id=project_id, **milestone) for milestone in milestones]
        elif page_num is not None:
            return Folder(token=self.session.token).list(page_num=page_num)
        else:
            raise ValueError('Either project_id or page_num must be specified')

    """
    Experiment API
    """
    def add_experiment(self, project_id, folder_id, title, description=None):
        return Experiment(token=self.session.token, project_id=project_id, milestone_id=folder_id,
                          title=title, description=description).register()

    def get_experiment(self, experiment_id):
        return Experiment(token=self.session.token, id=experiment_id).get()

    def find_experiment(self, name):
        return Experiment(token=self.session.token).list(name=name)

    def update_experiment(self, experiment_id, title, description=None):
        return Experiment(token=self.session.token, id=experiment_id, title=title, description=description).update()

    def list_experiments(self, folder_id=None, page_num=None):
        if folder_id is not None:
            experiments = self.get_folder(folder_id=folder_id).experiments
            assert isinstance(experiments, list)
            return [Experiment(token=self.session.token, milestone_id=folder_id, **experiment)
                    for experiment in experiments]
        elif page_num is not None:
            return Experiment(token=self.session.token).list(page_num=page_num)
        else:
            raise ValueError('Either folder_id or page_num must be specified')

    """
    Section (ExperimentProcedure / ElementContainer)
    """
    def add_section(self, experiment_id, name, section_type='text', container_type='Projects::Experiment',
                    member_id='1', owner_id=1, **kwargs):
        return Section(token=self.session.token,
                       container_id=experiment_id,
                       name=name,
                       section_type=section_type,
                       container_type=container_type,
                       member_id=member_id,
                       owner_id=owner_id, **kwargs).register()

    def find_section(self, name):
        return Section(token=self.session.token).list(name=name)

    def get_section(self, section_id):
        return Section(token=self.session.token, id=section_id).get()

    def update_section(self, section_id, name, **kwargs):
        return Section(token=self.session.token, id=section_id, name=name, **kwargs).update()

    def list_sections(self, experiment_id=None, page_num=None):
        if experiment_id is not None:
            experiment_procedures = self.get_experiment(experiment_id=experiment_id).experiment_procedures
            assert isinstance(experiment_procedures, list)
            return [Section(token=self.session.token, container_id=experiment_id, **experiment['experiment_procedure'])
                    for experiment in experiment_procedures]
        elif page_num is not None:
            return Section(token=self.session.token).list(page_num=page_num)
        else:
            raise ValueError('Either experiment_id or page_num must be specified')

    """
    Element API
    """
    def add_element(self, section_id, data, element_type='text', container_type='ExperimentProcedure', **kwargs):
        return Element(token=self.session.token,
                       container_id=section_id,
                       data=data,
                       element_type=element_type,
                       container_type=container_type, **kwargs).register()

    def find_element(self, name):
        return Element(token=self.session.token).list(name=name)

    def get_element(self, element_id):
        return Element(token=self.session.token, id=element_id).get()

    def update_element(self, element_id, name, **kwargs):
        return Element(token=self.session.token, id=element_id, name=name, **kwargs).update()

    def list_elements(self, section_id=None, page_num=None):
        if section_id is not None:
            elements = self.get_section(section_id=section_id).elements
            assert isinstance(elements, list)
            return [Element(token=self.session.token, container_id=section_id, **element)
                    for element in elements]
        elif page_num is not None:
            return Element(token=self.session.token).list(page_num=page_num)
        else:
            raise ValueError('Either experiment_id or page_num must be specified')

