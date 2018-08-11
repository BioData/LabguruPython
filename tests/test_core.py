# tests/test_core.py

from labguru import Labguru, Session, UnAuthorizeException, Project
from labguru.error import NotFoundException
import pytest
import vcr


@pytest.fixture
def valid_labguru_session():
    return Session(
        token='0978d492429c3bf824db87f2036ae182994b92ce',
        url='https://jonathan.labguru.com/',
        admin=False,
        orders=False
    )


@pytest.fixture
def project_101():
    return Project(**{
        "id": 101,
        "uuid": "f6ddee4d-1ea7-47f2-9519-ea6a377ed151",
        "title": "FtsH function in Chloroplasts",
        "user": 371,
        "description": "one of the first widely used E. coli cloning vectors.",
        "created_at": "2018-07-17",
        "owner_id": 31,
        "milestones": [],
        "comments": [],
        "experiment_procedures": [],
        "attachments": [],
        "archived": False,
        "api_url": "/api/v1/projects/101",
        "viewers": [],
        "owner": {}
    })


@vcr.use_cassette('tests/vcr_cassettes/labguru-session.yml')
def test_labguru_login(valid_labguru_session):
    lab = Labguru(login='xtutran@gmail.com', password='Password123')
    assert lab.session.token != '-1', 'Auth token should not be -1'
    assert lab.session.token == valid_labguru_session.token
    assert lab.session.url == valid_labguru_session.url
    assert lab.session.admin == valid_labguru_session.admin
    assert lab.session.orders == valid_labguru_session.orders


def test_labguru_login_fail():
    with pytest.raises(UnAuthorizeException):
        lab = Labguru(login='abc@abc.com', password='abc123')


@vcr.use_cassette('tests/vcr_cassettes/labguru-get-project-101.yml')
def test_labguru_get_project(project_101):
    lab = Labguru(login='xtutran@gmail.com', password='Password123')
    project = lab.get_project('101')
    assert project.id == project_101.id
    assert project.title == project_101.title
    assert project.description == project_101.description


def test_labguru_get_project_fail():
    lab = Labguru(login='xtutran@gmail.com', password='Password123')
    with pytest.raises(NotFoundException):
        project = lab.get_project('102')
