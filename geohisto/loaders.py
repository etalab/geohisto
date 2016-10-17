import csv

from .constants import (
    START_DATE, END_DATE, START_DATETIME, END_DATETIME,  SEPARATOR
)
from .models import Towns, Town, Record
from .utils import convert_date, convert_datetime, convert_name_with_article


def load_towns(filename='sources/france2016.txt'):
    """
    Load all towns from `filename` into an OrderedDict of `Town`s namedtuples.

    Warning: default file contains outdated towns but NOT renamed ones.
    """
    towns = Towns()
    with open(filename, encoding='cp1252') as file:
        for line in csv.DictReader(file, delimiter='\t'):
            actual = int(line['ACTUAL'])
            if actual == 9:  # Cantonal fraction.
                continue  # Skip for the moment.
            town = Town(**{
                'id': (line['DEP'] + line['COM'] + SEPARATOR
                       + START_DATE.isoformat()),
                'depcom': line['DEP'] + line['COM'],
                'actual': actual,
                'modification': 0,
                'ancestors': '',
                'successors': '',
                'start_date': START_DATE,
                'end_date': END_DATE,
                'start_datetime': START_DATETIME,
                'end_datetime': END_DATETIME,
                'dep': line['DEP'],
                'com': line['COM'],
                'nccenr': convert_name_with_article(line),
                'population': 'NULL'
            })
            towns[town.id] = town
    return towns


def load_history(filename='sources/historiq2016.txt'):
    """Load all towns from `filename` into a list of `Record`s."""
    history = []
    with open(filename, encoding='cp1252') as file:
        for line in csv.DictReader(file, delimiter='\t'):
            effdate = convert_date(line['EFF'])
            record = Record(**{
                'depcom': line['DEP'] + line['COM'],
                'mod': int(line['MOD']),
                'eff': convert_datetime(line['EFF']),
                'effdate': effdate,
                'nccoff': line['NCCOFF'],
                'nccanc': line['NCCANC'],
                'comech': line['COMECH'],
                'dep': line['DEP'],
                'com': line['COM'],
                'depanc': line['DEPANC'],
                'nbcom': line['NBCOM'],
                'rangcom': line['RANGCOM'],
            })
            history.append(record)
    return history


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


def load_populations():
    """Load all populations into a dedicated dict."""
    return {
        'metropole': load_population_from('sources/population_metropole.csv'),
        'arrondissements': load_population_from(
            'sources/population_arrondissements.csv'),
        'dom': load_population_from('sources/population_dom.csv'),
        'mortes': load_population_from('sources/population_mortes.csv')
    }
