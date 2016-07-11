#!/usr/bin/env python
import csv
from collections import defaultdict
from datetime import date
from itertools import islice

# The first date in history records is 1943-08-12. We need these
# boundaries to deal with ranges related to renamed towns
# with the same INSEE (DEP+COM) codes.
START_DATE = date(1943, 1, 1)
END_DATE = date(2020, 1, 1)


def _chunks(string, num):
    """Split a given `string` by `num` characters and return a list."""
    return [string[start:start+num] for start in range(0, len(string), num)]


def _convert_date(string):
    """
    Convert '01-01-2016' to a Python `datetime.date` object.

    For the particular case where there are multiple dates within the
    same key, we return a list of `datetime.date` object.
    """
    if not string or string == '         .':  # Yes, it happens once!
        return ''

    if len(string) > 10:
        return [_convert_date(chunk) for chunk in _chunks(string, 10)]

    return date(*reversed([int(i) for i in string.split('-')]))


def _convert_leg(string):
    """
    Convert 'L01-01-2016' to a Python tuple ('L', `datetime.date`).

    For the particular case where there are multiple dates within the
    same key, we return a list of tuples.
    """
    if not string:
        return ''

    if len(string) > 11:
        return [_convert_leg(chunk) for chunk in _chunks(string, 11)]

    return string[0], _convert_date(string[1:])


def _has_been_hard_renamed(town, history):
    """Return `True` in case of a rename without any other operation."""
    return int(history['MOD']) in (100, 110)


def _has_been_renamed(town, history):
    """Return `True` in case of a rename with the same INSEE code."""
    return (int(history['MOD']) == 331
            and history['NCCOFF'] != town[0]['NCCENR'])


def _has_ancestor(town, history):
    """Return `True` in case of a merge with a different name."""
    return (int(history['MOD']) in (320, 340, 341)
            and town[0]['NCCENR'] != towns[history['COMECH']][0]['NCCENR'])


def _add_same_ancestor(town, history):
    """
    Enrich the `town` with a copy of itself.

    Keeping the old name and updating dates.
    """
    current = town[0]
    same_ancestor = current.copy()
    same_ancestor['ANCESTORS'] = []
    same_ancestor['END_DATE'] = history['EFF']
    # Take the `OFF`icial name if different from actual,
    # otherwise fallback on the `ANC`ient one.
    if same_ancestor['NCCENR'] != history['NCCOFF']:
        same_ancestor['NCCENR'] = history['NCCOFF']
    else:
        same_ancestor['NCCENR'] = history['NCCANC']
    current['START_DATE'] = history['EFF']
    town.append(same_ancestor)


def _add_ancestor(town, history):
    """Add an ancestor to a given `town`, updating dates."""
    current = town[0]
    ancestor = towns[history['COMECH']][0]
    ancestor['END_DATE'] = history['EFF']
    current['START_DATE'] = history['EFF']
    current['ANCESTORS'].append(history['COMECH'])


def _compute_population(populations, population_id, town=None):
    """
    Retrieve the population from `populations` dict cast as an integer.

    If the `population_id` is missing and `town` is available, we try
    to compute the population based on ancestors (renames + merges).
    """
    # If the population is already available, return it.
    population = int(populations.get(population_id, 0))
    if population or town is None:
        return population
    # Otherwise sum populations from renamed + ancestors towns.
    population = 0
    for t in town[1:]:
        population_id = t['DEP'] + t['COM'] + t['NCCENR']
        population += _compute_population(populations, population_id)
    for ancestor in town[0]['ANCESTORS']:
        ancestor = towns[ancestor][0]
        population_id = ancestor['DEP'] + ancestor['COM'] + ancestor['NCCENR']
        population += _compute_population(populations, population_id)
    return population


def load_towns_from(filename):
    """
    Load all towns from `filename` into a dict of lists.

    Warning: that file contains outdated towns but NOT renamed ones.
    """
    towns = defaultdict(list)
    with open(filename, encoding='cp1252') as file:
        for town in csv.DictReader(file, delimiter='\t'):
            actual = int(town['ACTUAL'])
            town['ANCESTORS'] = []
            town['START_DATE'] = START_DATE
            town['END_DATE'] = END_DATE
            if actual == 9:  # Cantonal fraction.
                continue  # Skip for the moment.
            # Beware that the `DEP` + `COM` combination is not unique,
            # hence the defaultdict list.
            towns[town['DEP'] + town['COM']].append(town)
    return towns


def compute_history_from(filename, towns):
    """
    Compute ancestors for each `towns` for renamed and merged towns.

    We are looping over the `filename` to detect renaming and merging
    actions within the past, enriching the given town with dates
    of these events and keys of ascendants.
    """
    with open(filename, encoding='cp1252') as file:
        for history in csv.DictReader(file, delimiter='\t'):
            town = towns[history['DEP'] + history['COM']]
            history['DTR'] = _convert_date(history['DTR'])
            history['EFF'] = _convert_date(history['EFF'])
            history['JO'] = _convert_date(history['JO'])
            history['LEG'] = _convert_leg(history['LEG'])
            if _has_been_hard_renamed(town, history):
                _add_same_ancestor(town, history)
            elif _has_been_renamed(town, history):
                _add_same_ancestor(town, history)
            elif _has_ancestor(town, history):
                _add_ancestor(town, history)
    return towns


def load_population_from(filename):
    """
    Load populations from `filename` into a dict.

    We use the name `DEPCOM` + `LIBMIN` as key because we cannot rely on
    `DEPCOM` only, it is not unique (recycled on towns' merges).
    """
    populations = {}
    with open(filename) as population:
        for item in csv.DictReader(population, delimiter=';'):
            populations[item['DEPCOM'] + item['LIBMIN']] = item['PMUN13']
    return populations


def write_results_on(filename, towns, populations):
    """
    Write the `filename` with CSV formatted informations.

    With the generated file, you will be able to retrace the history of
    a given INSEE code with renames and merges.

    Each town has an associated population, sometimes computed from
    population of ancestors.
    """
    with open(filename, 'w') as csvfile:
        fieldnames = [
            'DIRECTION', 'NAME', 'START_DATE', 'END_DATE', 'INSEE_CODE',
            'POPULATION'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        write = writer.writerow

        for id, town in sorted(towns.items()):
            current = town[0]
            # Root elements are the one still in use, skip others.
            if not current['END_DATE'] == END_DATE:
                continue
            population_id = id + current['NCCENR']
            population = _compute_population(populations, population_id, town)
            # Main entry.
            write({
                'DIRECTION': '==',
                'NAME': current['NCCENR'],
                'START_DATE': current['START_DATE'],
                'END_DATE': current['END_DATE'],
                'INSEE_CODE': id,
                'POPULATION': population
            })
            # Add an entry for each rename (same id).
            for t in town[1:]:
                id = t['DEP'] + t['COM']
                population_id = id + t['NCCENR']
                population = _compute_population(populations, population_id)
                write({
                    'DIRECTION': '<-',
                    'NAME': t['NCCENR'],
                    'START_DATE': t['START_DATE'],
                    'END_DATE': t['END_DATE'],
                    'INSEE_CODE': id,
                    'POPULATION': population
                })

            # Add an entry for each ancestor (different id).
            for ancestor in current['ANCESTORS']:
                ancestor = towns[ancestor][0]
                id = ancestor['DEP'] + ancestor['COM']
                population_id = id + ancestor['NCCENR']
                population = _compute_population(populations, population_id)
                write({
                    'DIRECTION': '->',
                    'NAME': ancestor['NCCENR'],
                    'START_DATE': ancestor['START_DATE'],
                    'END_DATE': ancestor['END_DATE'],
                    'INSEE_CODE': id,
                    'POPULATION': population
                })


def generate_head_results_from(filename, nb_of_lines=100):
    """
    Equivalent of `head` using Python.

    The passed `filename` will have a `_head` suffix added for the
    newly generated extract.
    """
    filepath, extension = filename.split('.')
    filename_out = filepath + '_head.' + extension
    with open(filename) as csvfile, \
            open(filename_out, 'w') as csvfileout:
        head = islice(csvfile, nb_of_lines)
        csvfileout.write(''.join(head))


if __name__ == '__main__':
    towns = load_towns_from('sources/france2016.txt')
    towns = compute_history_from('sources/historiq2016.txt', towns)
    populations = load_population_from('sources/population_metropole.csv')
    write_results_on('exports/towns/towns.csv', towns, populations)
    generate_head_results_from('exports/towns/towns.csv')
