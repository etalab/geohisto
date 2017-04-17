from datetime import date, datetime

from geohisto.constants import FUSION_ASSOCIATION_ASSOCIATED, CREATION


def test_initial_load(history_list):
    assert len(history_list) == 15673


def test_contains_first_last_items(history_list):
    amareins = history_list[0]
    cilaos = history_list[-1]
    assert amareins.mod == FUSION_ASSOCIATION_ASSOCIATED
    assert amareins.nccoff == 'Amareins'
    assert amareins.nccanc == ''
    assert amareins.comech == '01165'
    assert amareins.eff == datetime(1974, 1, 1, 0, 0)
    assert amareins.effdate == date(1974, 1, 1)
    assert cilaos.mod == CREATION
    assert cilaos.nccoff == 'Cilaos'
    assert cilaos.comech == '97414'
    assert cilaos.eff == datetime(1965, 2, 5, 0, 0)
    assert cilaos.effdate == date(1965, 2, 5)


def test_logic_related_to_last(history_list):
    amareins = history_list[0]
    cilaos = history_list[-1]
    arboys1 = history_list[6]
    arboys2 = history_list[7]
    assert amareins.last is None
    assert cilaos.last is None
    assert arboys1.last is not None
    assert not arboys1.last
    assert arboys2.last is not None
    assert arboys2.last
