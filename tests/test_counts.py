"""Tests related to counting towns in results."""
from datetime import datetime


def len_at_date(towns, year, month, day):
    return len(list(towns.valid_at(datetime(year, month, day))))


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
        '1962': (len_at_date(towns, 1962, 3, 7), 38076),
        '1968': (len_at_date(towns, 1968, 3, 1), 37823),
        '1975': (len_at_date(towns, 1975, 1, 1), 36407),
        '1982': (len_at_date(towns, 1982, 1, 1), 36547),
        '1985': (len_at_date(towns, 1985, 3, 1), 36614),
        '1990': (len_at_date(towns, 1990, 3, 1), 36664),
        '1994': (len_at_date(towns, 1994, 1, 1), 36673),
        '1999': (len_at_date(towns, 1999, 1, 1), 36679),
        '2000': (len_at_date(towns, 2000, 1, 1), 36680),
        '2001': (len_at_date(towns, 2001, 1, 1), 36677),
        '2002': (len_at_date(towns, 2002, 1, 1), 36679),
        '2003': (len_at_date(towns, 2003, 1, 1), 36678),
        '2004': (len_at_date(towns, 2004, 1, 1), 36682),
        '2005': (len_at_date(towns, 2005, 1, 1), 36684),
        '2006': (len_at_date(towns, 2006, 1, 1), 36685),
        '2007': (len_at_date(towns, 2007, 1, 1), 36683),
        '2008': (len_at_date(towns, 2008, 1, 1), 36681),
        '2009': (len_at_date(towns, 2009, 1, 1), 36682),
        '2010': (len_at_date(towns, 2010, 1, 1), 36682),
        '2011': (len_at_date(towns, 2011, 1, 1), 36680),
        '2012': (len_at_date(towns, 2012, 1, 1), 36700),
        '2013': (len_at_date(towns, 2013, 1, 1), 36681),
        '2014': (len_at_date(towns, 2014, 1, 1), 36681),
        '2015': (len_at_date(towns, 2015, 1, 1), 36658),
        '2016': (len_at_date(towns, 2016, 1, 1), 35885),
        '2017': (len_at_date(towns, 2017, 1, 1), 35416)
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
