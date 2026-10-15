import pytest

from labguru import Labguru
from labguru.exceptions import LabguruError

BASE = "https://demo.labguru.com"
FILTERS = [{"field": "title", "operator": "eq", "value": "x"}]


@pytest.mark.parametrize("ns", ["tags", "measurements", "visualizations"])
def test_filter_raises_where_list_is_blocked(ns):
    with pytest.raises(LabguruError):
        getattr(Labguru(url=BASE, token="t0k"), ns).filter(FILTERS)
