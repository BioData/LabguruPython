LabguruPython Repository
========================

This project is a Python wrapper of Labguru API

`Learn more <https://my.labguru.com/api/docs/>`_.

---------------

## Installation

You can install LabguruPython from github with:


``` sh
# clone repo
git clone https://github.com/BioData/LabguruPython.git

cd LabguruPython

# install required packages
pip install -r requirements.tx

# install LabguruPython
python setup.py install

```

Load LabguruPython

``` python
import labguru
```

# Authenticate

First get an authentication token using labguru_authenticate.

``` python
lab = Labguru(login="my@@email.com", password="mypassword")
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
project = lab.find_project(name="My new project")

print(project)
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
folder = lab.find_folder(name="My new folder")

print(folder)
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
experiment = lab.find_experiment(name="My new experiment")

print(experiment)
```

Update a experiment

``` python
experiment_old = lab.get_experiment(experiment_id='1')
print(experiment_old.id, experiment_old.title)

experiment_update = lab.update_experiment(experiment_id='1', title="Update new experiment title")

print(experiment_update.id, experiment_update.title)
```

## Experiment procedures

Update soon

## Elements

Update soon
