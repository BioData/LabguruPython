# tests/test_core.py

from labguru import Labguru, Session, UnAuthorizeException
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
