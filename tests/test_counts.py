"""Tests related to counting towns in results."""
from datetime import datetime


def test_counts(towns):
    """
    Test counting towns for a give date.

    Reference:
    https://fr.wikipedia.org/wiki/Nombre_de_communes_en_France↩
    #.C3.89volution_du_nombre_de_communes

    Easy diff re-computing:
    pprint.pprint({year: count-expect for year, (count, expect) in expected.items()})  # NOQA
    """
    expected = {
        '1962': (len(towns.valid_at(datetime(1962, 3, 7, 0, 0, 0))), 38076),
        '1968': (len(towns.valid_at(datetime(1968, 3, 1, 0, 0, 0))), 37823),
        '1975': (len(towns.valid_at(datetime(1975, 1, 1, 0, 0, 0))), 36407),
        '1982': (len(towns.valid_at(datetime(1982, 1, 1, 0, 0, 0))), 36547),
        '1985': (len(towns.valid_at(datetime(1985, 3, 1, 0, 0, 0))), 36614),
        '1990': (len(towns.valid_at(datetime(1990, 3, 1, 0, 0, 0))), 36664),
        '1994': (len(towns.valid_at(datetime(1994, 1, 1, 0, 0, 0))), 36673),
        '1999': (len(towns.valid_at(datetime(1999, 1, 1, 0, 0, 0))), 36679),
        '2000': (len(towns.valid_at(datetime(2000, 1, 1, 0, 0, 0))), 36680),
        '2001': (len(towns.valid_at(datetime(2001, 1, 1, 0, 0, 0))), 36677),
        '2002': (len(towns.valid_at(datetime(2002, 1, 1, 0, 0, 0))), 36679),
        '2003': (len(towns.valid_at(datetime(2003, 1, 1, 0, 0, 0))), 36678),
        '2004': (len(towns.valid_at(datetime(2004, 1, 1, 0, 0, 0))), 36682),
        '2005': (len(towns.valid_at(datetime(2005, 1, 1, 0, 0, 0))), 36684),
        '2006': (len(towns.valid_at(datetime(2006, 1, 1, 0, 0, 0))), 36685),
        '2007': (len(towns.valid_at(datetime(2007, 1, 1, 0, 0, 0))), 36683),
        '2008': (len(towns.valid_at(datetime(2008, 1, 1, 0, 0, 0))), 36681),
        '2009': (len(towns.valid_at(datetime(2009, 1, 1, 0, 0, 0))), 36682),
        '2010': (len(towns.valid_at(datetime(2010, 1, 1, 0, 0, 0))), 36682),
        '2011': (len(towns.valid_at(datetime(2011, 1, 1, 0, 0, 0))), 36680),
        '2012': (len(towns.valid_at(datetime(2012, 1, 1, 0, 0, 0))), 36700),
        '2013': (len(towns.valid_at(datetime(2013, 1, 1, 0, 0, 0))), 36681),
        '2014': (len(towns.valid_at(datetime(2014, 1, 1, 0, 0, 0))), 36681),
        '2015': (len(towns.valid_at(datetime(2015, 1, 1, 0, 0, 0))), 36658),
        '2016': (len(towns.valid_at(datetime(2016, 1, 1, 0, 0, 0))), 35885),
        '2017': (len(towns.valid_at(datetime(2017, 1, 1, 0, 0, 0))), 35416)
    }

    # If you edit these count results, be sure that it reduces the
    # difference with Wikipedia's numbers that we make the diff from.
    current_diff = {
        '1962': 60,
        '1968': 61,
        '1975': 157,
        '1982': 58,
        '1985': 58,
        '1990': 60,
        '1994': 60,
        '1999': 60,
        '2000': 61,
        '2001': 61,
        '2002': 61,
        '2003': 61,
        '2004': 61,
        '2005': 61,
        '2006': 61,
        '2007': 61,
        '2008': 62,
        '2009': 62,
        '2010': 62,
        '2011': 62,
        '2012': 45,
        '2013': 45,
        '2014': 46,
        '2015': 45,
        '2016': 48,
        '2017': 45
    }
    for year in expected:
        assert expected[year][0] - expected[year][1] == current_diff[year]
