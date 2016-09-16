"""
Utils in use to convert/compute historical data.

Most of the cryptic keys in that script are documented here:
http://www.insee.fr/fr/methodes/nomenclatures/cog/documentation.asp↩
?page=telechargement/2016/doc/doc_variables.htm
"""
from datetime import date, datetime


def chunks(string, num):
    """Split a given `string` by `num` characters and return a list."""
    return [string[start:start+num] for start in range(0, len(string), num)]


def convert_date(string):
    """
    Convert '01-01-2016' to a Python `datetime.date` object.

    For the particular case where there are multiple dates within the
    same key, we return a list of `datetime` object.
    """
    if not string or string == '         .':  # Yes, it happens once!
        return ''

    if len(string) > 10:
        return [convert_date(chunk) for chunk in chunks(string, 10)]

    return date(*reversed([int(i) for i in string.split('-')]))


def convert_datetime(string):
    """
    Convert '01-01-2016' to a Python `datetime.datetime` object.

    For the particular case where there are multiple dates within the
    same key, we return a list of `datetime` object.
    """
    if not string or string == '         .':  # Yes, it happens once!
        return ''

    if len(string) > 10:
        return [convert_datetime(chunk) for chunk in chunks(string, 10)]

    return datetime(
        *list(reversed([int(i) for i in string.split('-')])) + [0, 0, 0])


def convert_leg(string):
    """
    Convert 'L01-01-2016' to a Python tuple ('L', `datetime`).

    For the particular case where there are multiple dates within the
    same key, we return a list of tuples.
    """
    if not string:
        return ''

    if len(string) > 11:
        return [convert_leg(chunk) for chunk in chunks(string, 11)]

    return string[0], convert_date(string[1:])


def convert_name_with_article(town):
    """Return the `town` name with optional article."""
    if town['ARTMIN']:
        # Special `L'` case, all other article require a space.
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
            successor = towns.get(successor_id)
            if successor:
                new_ancestors = (successor.ancestors
                                 and successor.ancestors + ';' + town.id
                                 or town.id)
                towns += successor._replace(ancestors=new_ancestors)
    return towns


def compute_population(populations, population_id,
                       towns, town=None, key='metropole'):
    """
    Retrieve the population from `populations` dict cast as an integer.

    Fallback on `arrondissements` and `dom` if no population is found.
    Finally, a population of `0` is added for listed dead towns.
    In case of unknown population the value `NULL` is returned.

    If the `population_id` is missing and `town` is available, we try
    to compute the population based on ancestors (renames + merges).
    The `key` is useful for the recursivity of the function in order to
    explore different `populations` sub-dictionnaries.

    WARNING: you have to compute population AFTER computing ancestors.
    """
    # If the population is already available, return it.
    population = int(populations[key].get(population_id, 0))
    if population:
        return population
    elif town is None:
        return 'NULL'

    # Otherwise sum populations from ancestors towns.
    population = 0
    if town.ancestors:
        for ancestor_id in town.ancestors.split(';'):
            ancestor = towns.get(ancestor_id)
            population_id = ancestor.depcom + ancestor.nccenr
            try:
                population += compute_population(
                    populations, population_id, towns)
            except TypeError:  # Returned population equals 'NULL'
                pass

    if not population:
        try:
            population += compute_population(
                populations, population_id, towns, key='arrondissements')
        except TypeError:  # Returned population equals 'NULL'
            pass
    if not population:
        try:
            population += compute_population(
                populations, population_id, towns, key='dom')
        except TypeError:  # Returned population equals 'NULL'
            pass
    if not population and population_id not in populations['mortes']:
        population = 'NULL'

    return population
