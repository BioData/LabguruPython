# tests/test_api.py

import pytest
from labguru import api


@pytest.mark.parametrize("endpoint, base, expected", [
    ('/api/v1/sessions.json', 'https://jonathan.labguru.com', 'https://jonathan.labguru.com/api/v1/sessions.json'),
    ('/api/v1/projects.json', 'https://labguru.com', 'https://labguru.com/api/v1/projects.json')
])
def test_normalise(endpoint, base, expected):
    assert api.normalise(endpoint, base) == expected
