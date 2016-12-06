"""
Utils in use to convert/compute historical data.

Most of the cryptic keys in that script are documented here:
https://www.insee.fr/fr/information/2114819#titre-bloc-10
"""
import csv
from datetime import date, datetime
from functools import wraps

from .constants import SEPARATOR

ACTIONS = {}


def iter_over_insee_csv_file(csv_filepath):
    """Open and enumerate over a CSV file located at `csv_filepath`."""
    with open(csv_filepath, encoding='cp1252') as csv_file:
        for i, data in enumerate(csv.DictReader(csv_file, delimiter='\t')):
            yield i, data


def in_case_of(*actions):
    """Decorator to register links between actions and codes."""
    def inner(func):
        for action in actions:
            ACTIONS[action] = func

        @wraps(func)
        def inner_func(towns, record):
            func(towns, record)
        return inner_func
    return inner


def convert_date(string):
    """Convert '01-01-2016' to a Python `datetime.date` object."""
    return date(*reversed([int(i) for i in string.split('-')]))


def convert_datetime(string):
    """Convert '01-01-2016' to a Python `datetime.datetime` object."""
    return datetime.combine(convert_date(string), datetime.min.time())


def convert_name_with_article(town):
    """Return the `town` name with optional article."""
    if town['ARTMIN']:
        # Special `L'` case, all other articles require a space.
        extra_space = int(town['TNCC']) != 5
        return '{article}{extra_space}{name}'.format(
            article=town['ARTMIN'][1:-1],
            extra_space=' ' if extra_space else '',
            name=town['NCCENR']
        )
    else:
        return town['NCCENR']


def compute_id(depcom, start_date):
    """Return the unique string id for a given `depcom` + `start_date`."""
    return 'COM{depcom}{separator}{start_date}'.format(
        depcom=depcom, separator=SEPARATOR, start_date=start_date.isoformat())


def compute_ancestors(towns):
    """
    Reverse the tree of successors to have ancestors.

    Useful to compute new populations for instance.
    """
    for town in towns.with_successors():
        for successor_id in town.successors.split(';'):
            successor = towns.retrieve(successor_id)
            if successor:
                successor = successor.add_ancestor(town.id)
                towns.upsert(successor)
            else:
                print('Successor not found for', town)
