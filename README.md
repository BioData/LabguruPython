LabguruPython Repository
========================

This project is a Python wrapper of Labguru API

`Learn more <https://my.labguru.com/api/docs/>`_.

---------------

## Installation

You can install LabguruPython from github with:


```

# clone repo
git clone https://github.com/BioData/LabguruPython.git

cd LabguruPython

# install LabguruPython
python setup.py install

```

Load LabguruPython

``` python
from labguru import Labguru
```

# Authenticate

First get an authentication token using labguru_authenticate.

``` python
lab = Labguru(login="my@email.com", password="mypassword")
```

# Experiment

## Project

List all projects

``` python
projects = lab.list_projects(page_num=1)

# print out project info
for project in projects:
    print(project.id, project.title)
```

Download project information

``` python
project_1 = lab.get_project(project_id='1')

print(project_1.id, project.title)
```

Start new project

``` python
project_new = lab.add_project(title="My new project", description="This project is an analysis of ...")

print(project_new)
```

Find a project by name

``` python
projects = lab.find_projects(name="My new project")

print(projects)
```

Update a project

``` python
project_old = lab.get_project(project_id='1')
print(project_old.id, project_old.title)

project_update = lab.update_project(project_id='1', title="Update new project title")

print(project_update.id, project_update.title)
```

## Folder

List all folders

``` python
# project_id=None or not specified - return all folders in all projects (default)
folders = lab.list_folders(project_id=91, page_num=1)

for folder in folders:
    print(folder)

```

Download folder information

``` python
folder_1 = lab.get_folder(folder_id = 31)

print(folder_1)
```

Start new folder

``` python
folder_new = lab.add_folder(project_id=91, title="My new folder", description="This folder is a test from LabguruPython")

print(folder_new)
```

Find a folder by name

``` python
folders = lab.find_folders(name="My new folder")

print(folders)
```

Update a folder

``` python
folder_old = lab.get_folder(folder_id='1')
print(folder_old.id, folder_old.title)

folder_update = lab.update_folder(folder_id='1', title="Update new folder title")

print(folder_update.id, folder_update.title)
```

## Experiment

List all experiments



``` python
# folder_id=None or not specified - return all experiments in all projects (default)
experiments = lab.list_experiments(folder_id=410, page_num=1)

for experiment in experiments:
    print(experiment)
```

Download experiment information

``` python
experiment_1 = lab.get_experiment(experiment_id=141)

print(experiment_1)
```

Start new experiment

``` python
experiment_new = lab.add_experiment(project_id=91, folder_id=41, title="My new experiment 26-7-2018", \
                                    description = "This experiment is a test from LabguruR  26-7-2018")
print(experiment_new)
```

Find a experiment by name

``` python
experiments = lab.find_experiments(name="My new experiment")

print(experiments)
```

Update a experiment

``` python
experiment_old = lab.get_experiment(experiment_id='1')
print(experiment_old.id, experiment_old.title)

experiment_update = lab.update_experiment(experiment_id='1', title="Update new experiment title")

print(experiment_update.id, experiment_update.title)
```

## Experiment procedures

Add section to experiment

``` python
section = lab.add_experiment_procedure(experiment_id=817, name='test1')

print(section)
```

Find section

``` python
sections = lab.find_experiment_procedures(name='test1')

print(sections)
```

Get section

``` python
section = lab.get_experiment_procedure(section_id=5514)

print(section)
```

Update section

``` python
section = lab.update_experiment_procedure(section_id=5514, name='new name')

print(section)
```

List sections

``` python
sections = lab.list_experiment_procedures(experiment_id=817, page_num=1)

print(sections)
```

## Elements

Add element to section

``` python
element = lab.add_element(section_id=5478, data=None, element_type='steps')

print(element)
```

Get element

``` python
elements = lab.get_element(element_id='1601')

print(elements)
```

Update element

``` python
element = lab.update_element(element_id=8117, name='text element', data='<p> add text </p>')

print(element)
```

List elements by type

``` python
elements = lab.get_elements_by_type(experiment_id=586, element_type='plate')

print(elements)
```

## Items

Add item

``` python
item = lab.add_inventory_item(name='cell_line_1', item_type='cell_lines')

print(item)
```

Get item

``` python
items = lab.get_inventory_item(item_id=329, item_type='cell_lines')

print(items)
```

Update item

``` python
item = lab.update_inventory_item(item_id=329, item_type='cell_lines', name='new name')

print(item)
```

List items

``` python
items = lab.list_inventory_items(item_type='cell_lines', page_num=1)

print(items)
```

## Datasets

List Datasets

``` python
datasets = lab.list_datsets(page_num=1)

print(datasets)
```

Get Datasets

``` python
dataset = lab.get_dataset(dataset_id=13)

print(dataset)
```

Add Dataset

``` python
dataset = lab.add_dataset(dataset_name="Table", data=df)

print(dataset)
```
