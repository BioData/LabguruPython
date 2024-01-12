# -*- coding: utf-8 -*-
from __future__ import print_function

from . import api
from .error import UnAuthorizeException
from .project import Project, Folder, Experiment, Procedure, Element
from .datasets import Datasets
from .inventory import InventoryItem, Stock
from .response import Session
from .validation import validate_required_fields, validate_names


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
        validate_names(action='create a new project', title=title)
        return Project(token=self.session.token, title=title, description=description).register()

    def get_project(self, project_id):
        validate_required_fields(action='get project', project_id=project_id)
        proj = Project(id=project_id, token=self.session.token)
        return proj.get()

    def find_projects(self, name):
        return Project(token=self.session.token).list(name=name)

    def update_project(self, project_id, title, description=None, **kwargs):
        validate_required_fields(action='update project', project_id=project_id)
        proj = Project(token=self.session.token, id=project_id, title=title, description=description, **kwargs)
        return proj.update()

    def archive_project(self):
        pass

    def list_projects(self, page_num):
        return Project(token=self.session.token).list(page_num=page_num)

    """
    Folder API
    """
    def add_folder(self, project_id, title, description=None):
        validate_names(action='create a new folder', title=title)
        validate_required_fields(action='create a new folder', project_id=project_id)
        return Folder(token=self.session.token, project_id=project_id, title=title, description=description).register()

    def get_folder(self, folder_id):
        validate_required_fields(action='get folder', folder_id=folder_id)
        return Folder(token=self.session.token, id=folder_id).get()

    def find_folders(self, name):
        return Folder(token=self.session.token).list(name=name)

    def update_folder(self, folder_id, title, description=None, **kwargs):
        validate_required_fields(action='update project', folder_id=folder_id)
        return Folder(token=self.session.token, id=folder_id, title=title, description=description, **kwargs).update()

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
        validate_names(action='create a new experiment', title=title)
        validate_required_fields(action='update project', folder_id=folder_id, project_id=project_id)
        return Experiment(token=self.session.token, project_id=project_id, milestone_id=folder_id,
                          title=title, description=description).register()

    def get_experiment(self, experiment_id):
        validate_required_fields(action='get experiment', experiment_id=experiment_id)
        return Experiment(token=self.session.token, id=experiment_id).get()

    def find_experiments(self, name):
        return Experiment(token=self.session.token).list(name=name)

    def update_experiment(self, experiment_id, title, description=None, **kwargs):
        validate_required_fields(action='update experiment', experiment_id=experiment_id)
        return Experiment(token=self.session.token, id=experiment_id, title=title, description=description,
                          **kwargs).update()

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
    Procedure (ExperimentProcedure / ElementContainer)
    """
    def add_experiment_procedure(self, container_id, name, section_type='text', container_type='Projects::Experiment',
                                 **kwargs):
        validate_names(action='create a new section', name=name)
        validate_required_fields(action='create a new section', container_id=container_id)
        return Procedure(token=self.session.token,
                         container_id=container_id,
                         name=name,
                         section_type=section_type,
                         container_type=container_type,
                         **kwargs).register()

    def find_experiment_procedures(self, name):
        return Procedure(token=self.session.token).list(name=name)

    def get_experiment_procedure(self, section_id):
        validate_required_fields(action='get section', section_id=section_id)
        return Procedure(token=self.session.token, id=section_id).get()

    def update_experiment_procedure(self, section_id, name, **kwargs):
        validate_required_fields(action='update section', section_id=section_id)
        return Procedure(token=self.session.token, id=section_id, name=name, **kwargs).update()

    def list_experiment_procedures(self, experiment_id=None, page_num=None):
        if experiment_id is not None:
            experiment_procedures = self.get_experiment(experiment_id=experiment_id).experiment_procedures
            assert isinstance(experiment_procedures, list)
            return [Procedure(token=self.session.token, container_id=experiment_id, **experiment['experiment_procedure'])
                    for experiment in experiment_procedures]
        elif page_num is not None:
            return Procedure(token=self.session.token).list(page_num=page_num)
        else:
            raise ValueError('Either experiment_id or page_num must be specified')

    """
    Element API
    """
    def add_element(self, section_id, data=None, element_type='text', container_type='ExperimentProcedure', **kwargs):
        validate_required_fields(action='add a new element', section_id=section_id)
        return Element(token=self.session.token,
                       container_id=section_id,
                       data=data,
                       element_type=element_type,
                       container_type=container_type, **kwargs).register()

    def find_elements(self, name):
        return Element(token=self.session.token).list(name=name)

    def get_element(self, element_id):
        validate_required_fields(action='get element', element_id=element_id)
        return Element(token=self.session.token, id=element_id).get()

    def update_element(self, element_id, name, **kwargs):
        validate_required_fields(action='update element', element_id=element_id)
        return Element(token=self.session.token, id=element_id, name=name, **kwargs).update_element()

    def list_elements(self, section_id=None, page_num=None):
        if section_id is not None:
            elements = self.get_experiment_procedure(section_id=section_id).elements
            assert isinstance(elements, list)
            return [Element(token=self.session.token, container_id=section_id, **element)
                    for element in elements]
        elif page_num is not None:
            return Element(token=self.session.token).list(page_num=page_num)
        else:
            raise ValueError('Either experiment_id or page_num must be specified')

    def get_elements_by_type(self, experiment_id, element_type):
        validate_required_fields(action='get elements by type', experiment_id=experiment_id)
        return Element(token=self.session.token, experiment_id=experiment_id, element_type=element_type).list_by_type()

    """
    Inventory Item API
    """
    def add_inventory_item(self, name, item_type):
        validate_names(action='create a new item', name=name, item_type=item_type)
        return InventoryItem(token=self.session.token, name=name, item_type=item_type).register()

    def get_inventory_item(self, item_id, item_type):
        validate_required_fields(action='get inventory item', item_id=item_id)
        validate_names(action='get inventory item', item_type=item_type)
        item = InventoryItem(id=item_id, token=self.session.token, item_type=item_type)
        return item.get()

    def find_inventory_items(self, name, item_type):
        validate_names(action='find inventory items', item_type=item_type)
        return InventoryItem(token=self.session.token, item_type=item_type).list(name=name)

    def update_inventory_item(self, item_id, name, item_type, **kwargs):
        validate_required_fields(action='update inventory item', item_id=item_id)
        validate_names(action='update inventory item', item_type=item_type)
        return InventoryItem(token=self.session.token, id=item_id, name=name, item_type=item_type, **kwargs).update()

    def list_inventory_items(self, item_type, page_num):
        validate_names(action='list inventory items', item_type=item_type)
        return InventoryItem(token=self.session.token, item_type=item_type).list(page_num=page_num)

    """
    Generic Inventory Item API
    """
    def add_inventory_generic_item(self, name, item_type):
        validate_names(action='add generic inventory item', item_type=item_type)
        return self.add_inventory_item(name=name, item_type=f'biocollections/{item_type}')

    def get_inventory_generic_item(self, item_id, item_type):
        validate_names(action='get generic inventory item', item_type=item_type)
        return self.get_inventory_item(item_id=item_id, item_type=f'biocollections/{item_type}')

    def find_inventory_generic_items(self, name, item_type):
        validate_names(action='find generic inventory items', item_type=item_type)
        return self.find_inventory_items(name=name, item_type=f'biocollections/{item_type}')

    def update_inventory_generic_item(self, item_id, name, item_type, **kwargs):
        validate_names(action='update generic inventory items', item_type=item_type)
        return self.update_inventory_item(item_id=item_id, name=name, item_type=f'biocollections/{item_type}', **kwargs)

    def list_inventory_generic_items(self, item_type, page_num):
        validate_names(action='list generic inventory items', item_type=item_type)
        return self.list_inventory_items(item_type=f'biocollections/{item_type}', page_num=page_num)

    """
    Stock API
    """
    def add_stock(self, stock_name, storage_id, storage_type, stockable_type, stockable_id, **kwargs):
        validate_names(action='create a new stock', stock_name=stock_name)
        validate_required_fields(action='create a new stock', storage_id=storage_id, storage_type=storage_type,
                                 stockable_type=stockable_type, stockable_id=stockable_id)
        return Stock(token=self.session.token,
                       name=stock_name,
                       storage_id=storage_id,
                       storage_type=storage_type,
                       stockable_type=stockable_type,
                       stockable_id=stockable_id, **kwargs).register()

    def find_stocks(self, name):
        return Stock(token=self.session.token).list(name=name)

    def get_stock(self, stock_id):
        validate_required_fields(action='get stock', stock_id=stock_id)
        return Stock(token=self.session.token, id=stock_id).get()

    def update_stock(self, stock_id, **kwargs):
        validate_required_fields(action='update stock', stock_id=stock_id)
        return Stock(token=self.session.token, id=stock_id, **kwargs).update()

    def list_stocks(self, page_num):
        return Stock(token=self.session.token).list(page_num=page_num)

    """
    Datasets API
    """

    def list_datasets(self, page_num):
        return Datasets(token=self.session.token).list(page_num=page_num)
    
    def get_dataset(self, dataset_id):
        validate_required_fields(action='get dataset', dataset_id=dataset_id)
        return Datasets(token=self.session.token, id=dataset_id).get()
    
    def add_dataset(self, dataset_name, dataset_id, data, **kwargs):
        validate_names(action='create a new dataset', dataset_name=dataset_name)
        validate_required_fields(action='create a new dataset', dataset_id=dataset_id)
        return Datasets(token=self.session.token,
                       name=dataset_name,
                       id=dataset_id,
                       data=data, **kwargs).register()