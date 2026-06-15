# tests/test_client.py
from labguru.exceptions import LabguruError, LabguruAPIError


def test_api_error_carries_status_and_message():
    err = LabguruAPIError(status_code=422, message="bad fields")
    assert err.status_code == 422
    assert "bad fields" in str(err)
    assert isinstance(err, LabguruError)
