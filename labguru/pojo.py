import abc
import json
import sys


class Response(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, token, **kwargs):
        self.token = token
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def to_dict(self):
        return dict(filter(lambda x: x[1] is not None, self.__dict__.items()))

    def __str__(self):
        return json.dumps(self.__dict__)


class Session(Response):
    def __init__(self, token, url, admin, orders):
        Response.__init__(self, token=token, url=url, admin=admin, orders=orders)
