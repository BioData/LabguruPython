import abc
import json
import sys
from . import api
from requests import HTTPError
from .error import UnAuthorizeException, NotFoundException, DuplicatedException


def filter_none(d):
    assert isinstance(d, dict)
    return dict(filter(lambda x: x[1] is not None, d.items()))


class Response(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, token, **kwargs):
        self.token = token
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def to_dict(self, used_fields=None):
        if used_fields is None:
            used_fields = ['token', 'endpoint', 'specific_endpoint']
        return dict(filter(lambda x: x[0] not in used_fields and x[1] is not None, self.__dict__.items()))

    def _add(self, endpoint, **kwargs):
        url = api.normalise(endpoint)
        data = filter_none(kwargs)
        data['token'] = self.token

        return api.request(url, data=data)

    def _get_or_update(self, endpoint, id, method='GET', **kwargs):
        url = api.normalise(endpoint.format(id=id))
        data = filter_none(kwargs)
        data['token'] = self.token
        try:
            return api.request(url, method=method, data=data)
        except HTTPError:
            raise NotFoundException('{name} {id} does not exist'.format(name=self.__class__, id=id))

    def find(self, endpoint, **kwargs):
        url = api.normalise(endpoint)
        data = filter_none(kwargs)
        data['token'] = self.token
        return api.request(url, method='GET', data=data)

    def __str__(self):
        return json.dumps(self.__dict__)


class Session(Response):
    def __init__(self, token, url, admin, orders, account_id, account_name, environment):
        Response.__init__(self, token=token, url=url, admin=admin, orders=orders, account_id=account_id, account_name=account_name,
                          environment=environment)
