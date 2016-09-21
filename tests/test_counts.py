"""Tests related to counting towns in results."""
from datetime import datetime

from geohisto.actions import do_all_actions

from .test_populations_load import (
    metropole_populations, arrondissements_populations, dom_populations,
    mortes_populations
)  # NOQA: fixtures.
from .test_towns_load import towns  # NOQA: fixtures.
from .test_history_load import history_list  # NOQA: fixtures.


def test_counts(towns, history_list):  # NOQA: fixtures.
    """
    Test counting towns for a give date.

    Reference:
    https://fr.wikipedia.org/wiki/Nombre_de_communes_en_France↩
    #.C3.89volution_du_nombre_de_communes
    """
    towns, history_list = do_all_actions(towns, history_list)

    # If you edit these count results, be sure that it reduces the
    # difference with Wikipedia's numbers (see comments).
    assert len(towns.valid_at(datetime(1962, 3, 7, 0, 0, 0))) == 38227  # 38076
    assert len(towns.valid_at(datetime(1968, 3, 1, 0, 0, 0))) == 37978  # 37823
    assert len(towns.valid_at(datetime(1975, 1, 1, 0, 0, 0))) == 36641  # 36407
    assert len(towns.valid_at(datetime(1982, 1, 1, 0, 0, 0))) == 36631  # 36547
    assert len(towns.valid_at(datetime(1985, 3, 1, 0, 0, 0))) == 36668  # 36614
    assert len(towns.valid_at(datetime(1990, 3, 1, 0, 0, 0))) == 36691  # 36664
    assert len(towns.valid_at(datetime(1994, 1, 1, 0, 0, 0))) == 36699  # 36673
    assert len(towns.valid_at(datetime(1999, 1, 1, 0, 0, 0))) == 36697  # 36679
    assert len(towns.valid_at(datetime(2000, 1, 1, 0, 0, 0))) == 36700  # 36680
    assert len(towns.valid_at(datetime(2001, 1, 1, 0, 0, 0))) == 36699  # 36677
    assert len(towns.valid_at(datetime(2002, 1, 1, 0, 0, 0))) == 36698  # 36679
    assert len(towns.valid_at(datetime(2003, 1, 1, 0, 0, 0))) == 36697  # 36678
    assert len(towns.valid_at(datetime(2004, 1, 1, 0, 0, 0))) == 36697  # 36682
    assert len(towns.valid_at(datetime(2005, 1, 1, 0, 0, 0))) == 36699  # 36684
    assert len(towns.valid_at(datetime(2006, 1, 1, 0, 0, 0))) == 36700  # 36685
    assert len(towns.valid_at(datetime(2007, 1, 1, 0, 0, 0))) == 36698  # 36683
    assert len(towns.valid_at(datetime(2008, 1, 1, 0, 0, 0))) == 36696  # 36681
    assert len(towns.valid_at(datetime(2009, 1, 1, 0, 0, 0))) == 36697  # 36682
    assert len(towns.valid_at(datetime(2010, 1, 1, 0, 0, 0))) == 36697  # 36682
    assert len(towns.valid_at(datetime(2011, 1, 1, 0, 0, 0))) == 36696  # 36680
    assert len(towns.valid_at(datetime(2012, 1, 1, 0, 0, 0))) == 36698  # 36700
    assert len(towns.valid_at(datetime(2013, 1, 1, 0, 0, 0))) == 36677  # 36681
    assert len(towns.valid_at(datetime(2014, 1, 1, 0, 0, 0))) == 36675  # 36681
    assert len(towns.valid_at(datetime(2015, 1, 1, 0, 0, 0))) == 36651  # 36658
    assert len(towns.valid_at(datetime(2016, 1, 1, 0, 0, 0))) == 35814  # 35885
