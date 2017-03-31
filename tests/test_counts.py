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
    assert len(towns.valid_at(datetime(1962, 3, 7, 0, 0, 0))) - 38076 == 58
    assert len(towns.valid_at(datetime(1968, 3, 1, 0, 0, 0))) - 37823 == 59
    assert len(towns.valid_at(datetime(1975, 1, 1, 0, 0, 0))) - 36407 == 157
    assert len(towns.valid_at(datetime(1982, 1, 1, 0, 0, 0))) - 36547 == 58
    assert len(towns.valid_at(datetime(1985, 3, 1, 0, 0, 0))) - 36614 == 57
    assert len(towns.valid_at(datetime(1990, 3, 1, 0, 0, 0))) - 36664 == 57
    assert len(towns.valid_at(datetime(1994, 1, 1, 0, 0, 0))) - 36673 == 57
    assert len(towns.valid_at(datetime(1999, 1, 1, 0, 0, 0))) - 36679 == 57
    assert len(towns.valid_at(datetime(2000, 1, 1, 0, 0, 0))) - 36680 == 58
    assert len(towns.valid_at(datetime(2001, 1, 1, 0, 0, 0))) - 36677 == 58
    assert len(towns.valid_at(datetime(2002, 1, 1, 0, 0, 0))) - 36679 == 58
    assert len(towns.valid_at(datetime(2003, 1, 1, 0, 0, 0))) - 36678 == 58
    assert len(towns.valid_at(datetime(2004, 1, 1, 0, 0, 0))) - 36682 == 58
    assert len(towns.valid_at(datetime(2005, 1, 1, 0, 0, 0))) - 36684 == 58
    assert len(towns.valid_at(datetime(2006, 1, 1, 0, 0, 0))) - 36685 == 58
    assert len(towns.valid_at(datetime(2007, 1, 1, 0, 0, 0))) - 36683 == 58
    assert len(towns.valid_at(datetime(2008, 1, 1, 0, 0, 0))) - 36681 == 59
    assert len(towns.valid_at(datetime(2009, 1, 1, 0, 0, 0))) - 36682 == 59
    assert len(towns.valid_at(datetime(2010, 1, 1, 0, 0, 0))) - 36682 == 59
    assert len(towns.valid_at(datetime(2011, 1, 1, 0, 0, 0))) - 36680 == 59
    assert len(towns.valid_at(datetime(2012, 1, 1, 0, 0, 0))) - 36700 == 43
    assert len(towns.valid_at(datetime(2013, 1, 1, 0, 0, 0))) - 36681 == 44
    assert len(towns.valid_at(datetime(2014, 1, 1, 0, 0, 0))) - 36681 == 43
    assert len(towns.valid_at(datetime(2015, 1, 1, 0, 0, 0))) - 36658 == 43
    assert len(towns.valid_at(datetime(2016, 1, 1, 0, 0, 0))) - 35885 == 53
