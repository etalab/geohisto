import csv
from collections import defaultdict

from .constants import (
    START_DATE, END_DATE, START_DATETIME, END_DATETIME, CREATION_DELEGATED_POLE
)
from .models import Towns, Town, Record
from .utils import (
    convert_date, convert_datetime, convert_name_with_article, compute_id,
    iter_over_insee_csv_file
)


def load_towns(filename='sources/france2016.txt'):
    """
    Load all towns from `filename` into an OrderedDict of `Town`s namedtuples.

    Warning: default file contains outdated towns but NOT renamed ones.
    """
    towns = Towns()
    for i, line in iter_over_insee_csv_file(filename):
        actual = int(line['ACTUAL'])
        if actual == 9:  # Cantonal fraction.
            continue  # Skip for the moment.
        town = Town(
            id=compute_id(line['DEP'] + line['COM'], START_DATE),
            depcom=line['DEP'] + line['COM'],
            actual=actual,
            modification=0,
            ancestors='',
            successors='',
            start_date=START_DATE,
            end_date=END_DATE,
            start_datetime=START_DATETIME,
            end_datetime=END_DATETIME,
            dep=line['DEP'],
            com=line['COM'],
            nccenr=convert_name_with_article(line),
            population='NULL',
            parents=''
        )
        towns[town.id] = town
    return towns


def load_history(filename='sources/historiq2016.txt'):
    """Load all towns from `filename` into a list of `Record`s."""
    history = []
    last_log = defaultdict(int)
    for i, line in iter_over_insee_csv_file(filename):
        effdate = convert_date(line['EFF'])
        depcom = line['DEP'] + line['COM']
        mod = int(line['MOD'])
        last = None
        # We need to know which one of the record is the last in case
        # of a `CREATION_DELEGATED_POLE` to delete the parent entry
        # only once the last element is dealt with.
        if mod == CREATION_DELEGATED_POLE:
            id = depcom + effdate.isoformat()
            last_log[id] += 1
            if id in last_log and last_log[id] == int(line['NBCOM']):
                last = True
            else:
                last = False
        record = Record(
            depcom=depcom,
            mod=mod,
            eff=convert_datetime(line['EFF']),
            effdate=effdate,
            nccoff=line['NCCOFF'],
            nccanc=line['NCCANC'],
            comech=line['COMECH'],
            dep=line['DEP'],
            com=line['COM'],
            depanc=line['DEPANC'],
            last=last,
        )
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


def load_counties(filename='exports/counties/counties.csv'):
    """Load counties from `filename` into a dict."""
    counties = defaultdict(list)
    with open(filename) as counties_csv:
        for line in csv.DictReader(counties_csv):
            counties[line['insee_code']].append(line)
    return counties
