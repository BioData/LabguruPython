import pytest

from labguru import Labguru
from labguru.exceptions import LabguruError

BASE = "https://demo.labguru.com"


@pytest.mark.parametrize("ns, call", [
    ("sections", lambda r: r.list()),
    ("elements", lambda r: r.list()),
    ("datasets", lambda r: r.update(1, {})),
    ("units", lambda r: r.update(1, {})),
    ("attachments", lambda r: r.list()),
    ("comments", lambda r: r.update(1, {})),
    ("members", lambda r: r.get(1)),
])
def test_verbs_without_an_endpoint_raise_before_calling(ns, call):
    with pytest.raises(LabguruError):
        call(getattr(Labguru(url=BASE, token="t0k"), ns))
