# -*- coding: utf-8 -*-
from __future__ import print_function

import json

from .response import Response


# Level 1
class InventoryItem(Response):
    def __init__(self, token=None, id=None, item_type=None, name=None, **kwargs):
        Response.__init__(self, token, **kwargs)
        self.name = name
        self.id = id
        self.endpoint = f'/api/v1/{item_type}.json'
        self.specific_endpoint = f'/api/v1/{item_type}/{{id}}.json'
        self.generic_item_endpoint = f'/api/v1/biocollections/{item_type}.json'
        self.generic_item_specific_endpoint = f'/api/v1/biocollections/{item_type}/{{id}}.json'

    def register(self):
        response = self._add(endpoint=self.endpoint, item=self.to_dict())
        return self.__class__(token=self.token, **response)

    def get(self):
        response = self._get_or_update(endpoint=self.specific_endpoint, id=self.id, method='GET')
        return self.__class__(token=self.token, **response)

    def list(self, name=None, page_num=None):
        response = self.find(endpoint=self.endpoint, name=name, page_num=page_num)
        if isinstance(response, list):
            return [self.__class__(token=self.token, **item) for item in response]
        else:
            return []

    def update(self):
        response = self._get_or_update(endpoint=self.specific_endpoint, id=self.id, method='PUT', item=self.to_dict())
        return self.__class__(token=self.token, **response)


# Level 2
class Stock(InventoryItem):
    def __init__(self, token=None, name=None, id=None, stockable_id=None, storage_id=None, storage_type=None, stockable_type=None, **kwargs):
        InventoryItem.__init__(self, token, stockable_id, **kwargs)
        self.id = id
        self.name = name
        self.storage_id = storage_id
        self.storage_type = storage_type
        self.stockable_id = stockable_id
        self.stockable_type = stockable_type
        self.endpoint = '/api/v1/stocks.json'
        self.specific_endpoint = '/api/v1/stocks/{id}.json'
