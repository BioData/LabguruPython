# -*- coding: utf-8 -*-

import requests
try:
    from urlparse import urljoin, urlparse
except ImportError as err:
    from urllib.parse import urlparse, urljoin


request_method = {
    'POST': (requests.post, 'json'),
    'PUT': (requests.put, 'json'),
    'GET': (requests.get, 'data')
}


def normalise(path, base='https://eu.labguru.com'):
    parsed_path = urlparse(path)
    parsed_base = urlparse(base)
    if parsed_path.scheme in ['http', 'https']:
        return parsed_path.geturl()
    elif parsed_base.scheme in ['http', 'https']:
        return urljoin(parsed_base.geturl(), parsed_path.geturl())
    else:
        raise ValueError('Malformed url: {0}/{1}'.format(base, path))


def request(url, method='POST', headers=None, auth=None, data=None):
    http_method, param = request_method[method]
    response = http_method(url=url, headers=headers, auth=auth, **{param: data})
    response.raise_for_status()
    try:
        json_data = response.json()

        assert isinstance(json_data, (dict, list))
        return json_data
    except ValueError:
        raise


def call(token, endpoint, method, *args, **kwargs):
    url = normalise(endpoint)
    kwargs['token'] = token
    return request(url, method=method, data=kwargs)

