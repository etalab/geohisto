"""Tests related to counting towns in results."""
from datetime import datetime


def test_counts(towns):
    """
    Test counting towns for a give date.

    Reference:
    https://fr.wikipedia.org/wiki/Nombre_de_communes_en_France↩
    #.C3.89volution_du_nombre_de_communes
    """
    # If you edit these count results, be sure that it reduces the
    # difference with Wikipedia's numbers that we make the diff from.
    i = 50
    assert len(towns.valid_at(datetime(1962, 3, 7, 0, 0, 0))) - 38076 == i + 12
    assert len(towns.valid_at(datetime(1968, 3, 1, 0, 0, 0))) - 37823 == i + 13
    assert len(towns.valid_at(datetime(1975, 1, 1, 0, 0, 0))) - 36407 == i + 112  # NOQA
    assert len(towns.valid_at(datetime(1982, 1, 1, 0, 0, 0))) - 36547 == i + 13
    assert len(towns.valid_at(datetime(1985, 3, 1, 0, 0, 0))) - 36614 == i + 13
    assert len(towns.valid_at(datetime(1990, 3, 1, 0, 0, 0))) - 36664 == i + 13
    assert len(towns.valid_at(datetime(1994, 1, 1, 0, 0, 0))) - 36673 == i + 13
    assert len(towns.valid_at(datetime(1999, 1, 1, 0, 0, 0))) - 36679 == i + 13
    assert len(towns.valid_at(datetime(2000, 1, 1, 0, 0, 0))) - 36680 == i + 14
    assert len(towns.valid_at(datetime(2001, 1, 1, 0, 0, 0))) - 36677 == i + 14
    assert len(towns.valid_at(datetime(2002, 1, 1, 0, 0, 0))) - 36679 == i + 14
    assert len(towns.valid_at(datetime(2003, 1, 1, 0, 0, 0))) - 36678 == i + 14
    assert len(towns.valid_at(datetime(2004, 1, 1, 0, 0, 0))) - 36682 == i + 14
    assert len(towns.valid_at(datetime(2005, 1, 1, 0, 0, 0))) - 36684 == i + 14
    assert len(towns.valid_at(datetime(2006, 1, 1, 0, 0, 0))) - 36685 == i + 14
    assert len(towns.valid_at(datetime(2007, 1, 1, 0, 0, 0))) - 36683 == i + 14
    assert len(towns.valid_at(datetime(2008, 1, 1, 0, 0, 0))) - 36681 == i + 15
    assert len(towns.valid_at(datetime(2009, 1, 1, 0, 0, 0))) - 36682 == i + 15
    assert len(towns.valid_at(datetime(2010, 1, 1, 0, 0, 0))) - 36682 == i + 15
    assert len(towns.valid_at(datetime(2011, 1, 1, 0, 0, 0))) - 36680 == i + 15
    assert len(towns.valid_at(datetime(2012, 1, 1, 0, 0, 0))) - 36700 == i - 2
    assert len(towns.valid_at(datetime(2013, 1, 1, 0, 0, 0))) - 36681 == i - 2
    assert len(towns.valid_at(datetime(2014, 1, 1, 0, 0, 0))) - 36681 == i - 1
    assert len(towns.valid_at(datetime(2015, 1, 1, 0, 0, 0))) - 36658 == i - 2
    assert len(towns.valid_at(datetime(2016, 1, 1, 0, 0, 0))) - 35885 == i
    assert len(towns.valid_at(datetime(2017, 1, 1, 0, 0, 0))) - 35416 == i - 4
