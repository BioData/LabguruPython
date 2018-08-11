from labguru import response

import pytest


@pytest.mark.parametrize("token,url,admin,orders", [
    ('0978d492429c3bf824db87f2036ae182994b92ce', 'https://jonathan.labguru.com/', False, False),
    ('0978d492429c3bf824db87f2036ae182994b92ce', 'https://labguru.com/', True, False),
])
def test_response(token, url, admin, orders):
    res = response.Response(token=token, url=url, admin=admin, orders=orders)
    assert res.url == url
