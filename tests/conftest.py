import pytest


@pytest.fixture(scope="module")
def vcr_config():
    """pytest-recording config for any @pytest.mark.vcr tests.

    Scrubs the auth token from recorded cassettes and refuses to hit the network
    on replay. The transport/resource tests use respx instead and don't need this;
    it's here for future recorded smoke tests against a real sandbox.
    """
    return {"filter_query_parameters": ["token"], "record_mode": "none"}
