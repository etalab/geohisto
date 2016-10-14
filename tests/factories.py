"""
Factories to generate fixtures data with less cumbersome.

Sane defaults are set for the generated namedtuples.
"""
from datetime import datetime

from geohisto.constants import START_DATE, END_DATE, SEPARATOR
from geohisto.models import Towns, Town, Record


def towns_factory(*town_factories):
    """Generate a `Towns` orderedlist from `town_factory` objects."""
    return Towns({
        town_factory.id: town_factory for town_factory in town_factories
    })


def town_factory(**custom):
    """Generate a `Town` namedtuple from `custom` parameters.

    Required parameters: `dep`, `com` and `nccenr`.
    """
    params = {
        'actual': '1',
        'modification': 0,
        'ancestors': '',
        'successors': '',
        'start_date': START_DATE,
        'end_date': END_DATE,
        'population': 'NULL'
    }
    custom['depcom'] = custom['dep'] + custom['com']
    params.update(custom)
    params['id'] = (params['depcom'] + SEPARATOR
                    + params['start_date'].isoformat())
    params['start_datetime'] = datetime.combine(params['start_date'],
                                                datetime.min.time())
    params['end_datetime'] = datetime.combine(params['end_date'],
                                              datetime.max.time())
    return Town(**params)


def record_factory(**custom):
    """Generate a `Record` namedtuple from `custom` parameters.

    Required parameters: `dep`, `com`, `mod`, `effdate`, `nccoff` and `nccanc`.
    """
    params = {
        'comech': '',
        'depanc': '',
        'nccanc': '',
        'nbcom': '',
        'rangcom': '',
    }
    params['depcom'] = custom['dep'] + custom['com']
    params.update(custom)
    params['eff'] = datetime.combine(params['effdate'], datetime.min.time())
    return Record(**params)
