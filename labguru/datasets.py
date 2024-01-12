from __future__ import print_function

import json

from .response import Response

class Datasets(Response):
    def __init__(self, token = None, id=None, name =None, **kwargs):
        Response.__init__(self, token, **kwargs)
        self.name = name
        self.id = id
        self.endpoint = f'/api/v1/datasets.json'
        self.specific_endpoint = f'/api/v1/datasets/{{id}}.json'

    def list(self, name=None, page_num=None):
        response = self.find(endpoint=self.endpoint, name=name, page_num=page_num)
        if isinstance(response, list):
            return [self.__class__(token=self.token, **item) for item in response]
        else:
            return []
    def get(self):
        response = self._get_or_update(endpoint=self.specific_endpoint, id=self.id, method='GET')
        return self.__class__(token=self.token, **response)
    
    def register(self):
        response = self._add(endpoint=self.endpoint, item=self.to_dict())
        return self.__class__(token=self.token, **response)
