"""
Utils in use to convert/compute historical data.

Most of the cryptic keys in that script are documented here:
http://www.insee.fr/fr/methodes/nomenclatures/cog/documentation.asp +
?page=telechargement/2016/doc/doc_variables.htm
"""
from datetime import date, datetime
from functools import wraps

ACTIONS = {}


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


def compute_ancestors(towns):
    """
    Reverse the tree of successors to have ancestors.

    Useful to compute new populations for instance.
    """
    for town in towns.with_successors():
        for successor_id in town.successors.split(';'):
            successor = towns.retrieve(successor_id)
            successor = successor.add_ancestor(town.id)
            towns.upsert(successor)
