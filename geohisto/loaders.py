import csv

from .constants import START_DATE, END_DATE
from .models import Towns, Town, HistoryList, History
from .utils import convert_date, convert_name_with_article


def load_towns(filename='sources/france2016.txt'):
    """
    Load all towns from `filename` into an OrderedDict of `Town`s namedtuples.

    Warning: default file contains outdated towns but NOT renamed ones.

    Example:

        {
            'ARTMAJ': "(L')",
            'CT': '08',
            'TNCC': '5',
            'MODIF': '0',
            'NCC': 'ABERGEMENT-CLEMENCIAT',
            'REG': '84',
            'COM': '001',
            'CHEFLIEU': '0',
            'RANG': '',
            'ARTICLCT': '',
            'POLE': '',
            'DEP': '01',
            'CDC': '0',
            'NCCCT': 'Châtillon-sur-Chalaronne',
            'NCCENR': 'Abergement-Clémenciat',
            'ARTMIN': "(L')",
            'ACTUAL': '1',
            'AR': '2'
        }

        becomes:

        Town(
            id='010011942-01-012020-01-01',
            actual=1,
            modification=0,
            ancestors='',
            successors='',
            start_date=datetime.date(1942, 1, 1),
            end_date=datetime.date(2020, 1, 1),
            depcom='01001',
            dep='01',
            com='001',
            nccenr="L'Abergement-Clémenciat",
            population=NULL
        )
    """
    towns = Towns()
    with open(filename, encoding='cp1252') as file:
        for line in csv.DictReader(file, delimiter='\t'):
            actual = int(line['ACTUAL'])
            if actual == 9:  # Cantonal fraction.
                continue  # Skip for the moment.
            town = Town(**{
                'id': (line['DEP'] + line['COM']
                       + START_DATE.isoformat() + END_DATE.isoformat()),
                'depcom': line['DEP'] + line['COM'],
                'actual': actual,
                'modification': 0,
                'ancestors': '',
                'successors': '',
                'start_date': START_DATE,
                'end_date': END_DATE,
                'dep': line['DEP'],
                'com': line['COM'],
                'nccenr': convert_name_with_article(line),
                'population': 'NULL'
            })
            towns += town
    return towns


def load_history(filename='sources/historiq2016.txt'):
    """
    Load all towns from `filename` into a list of `History`s namedtuples.

    Example:

        {
            'DTR': '01-01-2011',
            'JO': '',
            'NCCOFF': 'Plaisance',
            'DEPANC': '',
            'NCCANC': '',
            'DEP': '24',
            'C-LANC': '',
            'SUECH': '',
            'COM': '168',
            'CT': '19',
            'EFF': '01-01-2011',
            'NBCOM': '',
            'POPECH': '',
            'MOD': '360',
            'AR': '1',
            'RANGCOM': '',
            'CTANC': '',
            'ARRANC': '',
            'TNCCOFF': '0',
            'TNCCANC': '',
            'LEG': 'A24-02-2010',
            'C-LOFF': '',
            'COMECH': '24173'
        }

        becomes:

        History(
            depcom='24168',
            mod=360,
            eff=datetime.date(2011, 1, 1),
            nccoff='Plaisance',
            nccanc='',
            comech='24173',
            dep='24',
            com='168',
            depanc=''
        )
    """
    history_list = HistoryList()
    with open(filename, encoding='cp1252') as file:
        for line in csv.DictReader(file, delimiter='\t'):
            history = History(**{
                'depcom': line['DEP'] + line['COM'],
                'mod': int(line['MOD']),
                'eff': convert_date(line['EFF']),
                'nccoff': line['NCCOFF'],
                'nccanc': line['NCCANC'],
                'comech': line['COMECH'],
                'dep': line['DEP'],
                'com': line['COM'],
                'depanc': line['DEPANC']
            })
            history_list += history
    return history_list


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
