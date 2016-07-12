#!/usr/bin/env python
"""
Most of the cryptic keys in that script are documented here:
http://www.insee.fr/fr/methodes/nomenclatures/cog/documentation.asp↩
?page=telechargement/2016/doc/doc_variables.htm
"""
import csv
from collections import defaultdict
from datetime import date
from itertools import islice

from utils import (
    convert_date, convert_leg, compute_name, compute_population,
    has_been_hard_renamed, add_same_ancestor, has_been_renamed,
    add_ancestor, has_ancestor
)

# The first date in history records is 1943-08-12. We need these
# boundaries to deal with ranges related to renamed towns
# with the same INSEE (DEP+COM) codes.
START_DATE = date(1943, 1, 1)
END_DATE = date(2020, 1, 1)


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
            history['DTR'] = convert_date(history['DTR'])
            history['EFF'] = convert_date(history['EFF'])
            history['JO'] = convert_date(history['JO'])
            history['LEG'] = convert_leg(history['LEG'])
            if has_been_hard_renamed(town, history):
                add_same_ancestor(town, history)
            elif has_been_renamed(town, history):
                add_same_ancestor(town, history)
            elif has_ancestor(town, towns, history):
                add_ancestor(town, towns, history)
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
            name = compute_name(current)
            population_id = id + name
            population = compute_population(
                populations, population_id, towns, town)
            # Main entry.
            write({
                'DIRECTION': '==',
                'NAME': name,
                'START_DATE': current['START_DATE'],
                'END_DATE': current['END_DATE'],
                'INSEE_CODE': id,
                'POPULATION': population
            })
            # Add an entry for each rename (same id).
            for t in town[1:]:
                name = compute_name(t)
                population_id = id + name
                population = compute_population(
                    populations, population_id, towns)
                write({
                    'DIRECTION': '<-',
                    'NAME': name,
                    'START_DATE': t['START_DATE'],
                    'END_DATE': t['END_DATE'],
                    'INSEE_CODE': id,
                    'POPULATION': population
                })

            # Add an entry for each ancestor (different id).
            for ancestor in current['ANCESTORS']:
                ancestor = towns[ancestor][0]
                id = ancestor['DEP'] + ancestor['COM']
                name = compute_name(ancestor)
                population_id = id + name
                population = compute_population(
                    populations, population_id, towns)
                write({
                    'DIRECTION': '->',
                    'NAME': name,
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
    populations = {}
    populations['metropole'] = load_population_from(
        'sources/population_metropole.csv')
    populations['arrondissements'] = load_population_from(
        'sources/population_arrondissements.csv')
    populations['dom'] = load_population_from(
        'sources/population_dom.csv')
    populations['mortes'] = load_population_from(
        'sources/population_mortes.csv')
    write_results_on('exports/towns/towns.csv', towns, populations)
    generate_head_results_from('exports/towns/towns.csv')
