"""Tests related to counting towns in results."""
from datetime import datetime

from geohisto.actions import compute
from geohisto.loaders import load_towns


def test_counts(history_list):
    """
    Test counting towns for a give date.

    Reference:
    https://fr.wikipedia.org/wiki/Nombre_de_communes_en_France↩
    #.C3.89volution_du_nombre_de_communes
    """
    towns = load_towns()
    compute(towns, history_list)

    # If you edit these count results, be sure that it reduces the
    # difference with Wikipedia's numbers (see comments).
    assert len(towns.valid_at(datetime(1962, 3, 7, 1, 0, 0))) == 38130  # 38076
    assert len(towns.valid_at(datetime(1968, 3, 1, 1, 0, 0))) == 37876  # 37823
    assert len(towns.valid_at(datetime(1975, 1, 1, 1, 0, 0))) == 36554  # 36407
    assert len(towns.valid_at(datetime(1982, 1, 1, 1, 0, 0))) == 36596  # 36547
    assert len(towns.valid_at(datetime(1985, 3, 1, 1, 0, 0))) == 36662  # 36614
    assert len(towns.valid_at(datetime(1990, 3, 1, 1, 0, 0))) == 36712  # 36664
    assert len(towns.valid_at(datetime(1994, 1, 1, 1, 0, 0))) == 36721  # 36673
    assert len(towns.valid_at(datetime(1999, 1, 1, 1, 0, 0))) == 36727  # 36679
    assert len(towns.valid_at(datetime(2000, 1, 1, 1, 0, 0))) == 36729  # 36680
    assert len(towns.valid_at(datetime(2001, 1, 1, 1, 0, 0))) == 36726  # 36677
    assert len(towns.valid_at(datetime(2002, 1, 1, 1, 0, 0))) == 36728  # 36679
    assert len(towns.valid_at(datetime(2003, 1, 1, 1, 0, 0))) == 36727  # 36678
    assert len(towns.valid_at(datetime(2004, 1, 1, 1, 0, 0))) == 36731  # 36682
    assert len(towns.valid_at(datetime(2005, 1, 1, 1, 0, 0))) == 36733  # 36684
    assert len(towns.valid_at(datetime(2006, 1, 1, 1, 0, 0))) == 36734  # 36685
    assert len(towns.valid_at(datetime(2007, 1, 1, 1, 0, 0))) == 36732  # 36683
    assert len(towns.valid_at(datetime(2008, 1, 1, 1, 0, 0))) == 36731  # 36681
    assert len(towns.valid_at(datetime(2009, 1, 1, 1, 0, 0))) == 36732  # 36682
    assert len(towns.valid_at(datetime(2010, 1, 1, 1, 0, 0))) == 36732  # 36682
    assert len(towns.valid_at(datetime(2011, 1, 1, 1, 0, 0))) == 36730  # 36680
    assert len(towns.valid_at(datetime(2012, 1, 1, 1, 0, 0))) == 36733  # 36700
    assert len(towns.valid_at(datetime(2013, 1, 1, 1, 0, 0))) == 36714  # 36681
    assert len(towns.valid_at(datetime(2014, 1, 1, 1, 0, 0))) == 36715  # 36681
    assert len(towns.valid_at(datetime(2015, 1, 1, 1, 0, 0))) == 36691  # 36658
    assert len(towns.valid_at(datetime(2016, 1, 1, 1, 0, 0))) == 35923  # 35885
