from datetime import date, datetime

import pytest

from geohisto.loaders import load_history


@pytest.fixture
def history_list():
    return load_history()


def test_initial_load(history_list):
    assert len(history_list) == 12325


def test_contains_neuville(history_list):
    neuville = history_list.filter(depcom='10263')[0]
    assert neuville.mod == 100
    assert neuville.nccoff == 'Neuville-sur-Vanne'
    assert neuville.nccanc == 'Neuville-sur-Vannes'
    assert neuville.eff == datetime(2008, 10, 6, 0, 0, 0)
    assert neuville.effdate == date(2008, 10, 6)
