from datetime import date, datetime

from geohisto.constants import (
    FUSION_ASSOCIATION_SIMPLE_POLE, CREATION_DELEGATED_POLE
)


def test_initial_load(history_list):
    assert len(history_list) == 12325


def test_contains_first_last_items(history_list):
    plaisance = history_list[0]
    rouget = history_list[-1]
    assert plaisance.mod == FUSION_ASSOCIATION_SIMPLE_POLE
    assert plaisance.nccoff == 'Plaisance'
    assert plaisance.nccanc == ''
    assert plaisance.comech == '24173'
    assert plaisance.eff == datetime(2011, 1, 1, 0, 0)
    assert plaisance.effdate == date(2011, 1, 1)
    assert rouget.mod == CREATION_DELEGATED_POLE
    assert rouget.nccoff == 'Rouget-Pers'
    assert rouget.comech == '15150'
    assert rouget.eff == datetime(2016, 1, 1, 0, 0)
    assert rouget.effdate == date(2016, 1, 1)


def test_logic_related_to_last(history_list):
    plaisance = history_list[0]
    rouget = history_list[-1]
    saint_constant1 = history_list[-6]
    saint_constant2 = history_list[-5]
    assert plaisance.last is None
    assert rouget.last is not None
    assert rouget.last
    assert saint_constant1.last is not None
    assert not saint_constant1.last
    assert saint_constant2.last is not None
    assert saint_constant2.last
