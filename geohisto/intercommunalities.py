import csv
import logging
import re
import os

from datetime import datetime
from itertools import groupby

from .constants import END_REMOVED, INTERCOMMUNALITY_START_YEAR
from .models import Intercommunality, Intercommunalities, Towns


log = logging.getLogger(__name__)

'''
TODO:
    - handle more rules (see tests)
    - handle merges from `sources/epci/fusions.csv`
    - generate intermediate states (ie. town changes during the year)
    - recompute population from `pmun` instead of the current `ptot`
'''


RE_IN_PRENTHESIS = re.compile(r'(?:\(|\[)(.*?)(?:\)|\])')
RE_WITH_PRENTHESIS = re.compile(r'((?:\(|\[).*?(?:\)|\]))')

NAME_RULES = {
    'CC': 'Communauté de Communes',
    'CA': 'Communauté d\'Agglomération',
    'CU': 'Communauté Urbaine',
    'CV': 'Communauté de Villes',
    'DISTRICT': 'District',
    'METRO': 'Métropole',
    'METRO69': '',
    'MET69': '',
    'SAN': 'Syndicat d\'Agglomération Nouvelle',
}

# Order matters
DISTRICT_PREFIXES = (
    ('D u ', 'DISTRICT Urbain '),
    ('D U ', 'DISTRICT Urbain '),
    ('D ', 'DISTRICT '),
    ('Di ', 'DISTRICT '),
)

TYPOS = {
    'C C ': 'CC ',
    'C c': 'CC ',
    'C A ': 'CA ',
    'C a': 'CA',
    'C U ': 'CU ',
    'C V ': 'CV ',
    'S A N ': 'SAN ',
    'C Agglo ': 'Communauté d\'Agglomération ',
}

COMMON_PREFIXES = (
    'rural', 'rurale', 'ruraux', 'rurales',
    'urbain', 'urbaine', 'urbains', 'urbaines'
)

PREPOSITIONS = ('du ', 'de ', 'de la ', 'd\'', 'des ')
ALWAYS_LOWER = (
    'du', 'de', 'des', 'sur', 'sous', 'en', 'la', 'le', 'les', 'aux', 'au', 'à'
)
WITH_APOSTROPHE = ('d\'', 'l\'')

PRE_REPLACEMENTS = {
    '': '\'',
    '': 'œ',
    '.': ' ',
    ':': '',
    '"': '',
}

POST_REPLACEMENTS = {
    'Reg ': 'Région ',
    'Region ': 'Région ',
    'Cant ': 'Canton ',
    'Breon': 'Bréon',
    'Saone': 'Saône',
    'Vallee': 'Vallée',
    'D Or': 'd\'Or',
    'Indre - Brenne': 'Indre-Brenne',
    'Saône-Chalaronne': 'Saône Chalaronne',
}


def should_replace_kind(name, kind):
    return name.startswith(tuple(
        ' '.join((kind, prep)) for prep in PREPOSITIONS
    )) or name.lower().startswith(tuple(
        ' '.join((kind.lower(), prefix, prep)) for prep in PREPOSITIONS
        for prefix in COMMON_PREFIXES
    ))


def fix_typos(name):
    for typo, fix in TYPOS.items():
        if typo in name:
            name = name.replace(typo, fix)
    return name


def fix_word_casing(word):
    if any(word.lower().startswith(prefix) for prefix in WITH_APOSTROPHE):
        prefix, suffix = word.split('\'', 1)
        return '\''.join((prefix.lower(), suffix.capitalize()))
    elif word.lower() in ALWAYS_LOWER:
        return word.lower()
    elif word in NAME_RULES:
        return word.upper()
    else:
        return word.capitalize()


def fix_casing(name):
    return ' '.join(fix_word_casing(word) for word in name.split(' '))


def extract_name(line):
    """Extract and normalize an intercommunality name"""
    name = line['nom'].strip('\' ')
    for char, replacement in PRE_REPLACEMENTS.items():
        name = name.replace(char, replacement)
    kind = line['nature']
    name = fix_typos(name)
    name = ' '.join(name.split())  # replace multiple spaces
    if name.isupper():
        name = fix_casing(name)
    if line['nature'] == 'DISTRICT':
        for prefix, replacement in DISTRICT_PREFIXES:
            if name.startswith(prefix):
                name = name.replace(prefix, replacement, 1)
                break
    if name.startswith(kind):
        if should_replace_kind(name, kind):
            name = name.replace(kind, NAME_RULES[kind])
        else:
            name = name.replace('{0} '.format(kind), '')
    elif name.startswith(PREPOSITIONS):
        name = ' '.join((NAME_RULES[kind], name))
    elif name.lower().startswith(tuple(
            ' '.join((kind.lower(), prefix, prep)) for prep in PREPOSITIONS
            for prefix in COMMON_PREFIXES
            )):
        name = ' '.join((NAME_RULES[kind], name))
    if name.lower().startswith(COMMON_PREFIXES):
        name = ' '.join(name.split(' ')[1:])
    for char, replacement in POST_REPLACEMENTS.items():
        name = name.replace(char, replacement)
    # Removes acronyms except from Tours
    if not name.startswith('Tour'):
        name = re.sub(RE_WITH_PRENTHESIS, '', name).strip()
    # First char is always upper
    return name[0].upper() + name[1:]


def extract_acronym(line):
    """Extract acronym from parenthesis in name if present"""
    name = line['nom']
    if not name.startswith('Tour'):
        match = re.search(RE_IN_PRENTHESIS, name)
        return match.group(1).strip().upper() if match else None


def siren_key(line):
    return line['siren']


def load_intercommunalities_from(filename, year, towns):
    """
    Load EPCIs for a given year from a CSV file given its filename.
    """
    log.debug('Load intercommunalities from %s', filename)
    validity = datetime(year, 1, 1)
    # validity = datetime.combine(datetime(year, 1, 1), datetime.max.time())
    intercommunality = Intercommunality()
    # Filter towns only valid on the first of the year to speed up the lookup
    towns = Towns([(town.id, town) for town in towns.valid_at(validity)])
    with open(filename) as epci_csv:
        all_lines = csv.DictReader(epci_csv, delimiter=';', quotechar='"')
        # No need to sort CSV are already sorted by SIREN
        # all_lines = sorted(all_lines, key=siren_key)

        for siren, lines in groupby(all_lines, siren_key):
            for line in lines:
                if siren != intercommunality.siren:
                    intercommunality = Intercommunality(
                        siren=siren,
                        name=extract_name(line),
                        acronym=extract_acronym(line),
                        kind=line['nature'],
                        taxmodel=line['fiscalite'],
                        population=line['ptot']
                    )
                insee = line['insee'].zfill(5)
                attach_town(intercommunality, insee, validity, towns)
            yield intercommunality


def load_intercommunalities(towns, directory='sources/epci',
                            start=INTERCOMMUNALITY_START_YEAR, end=2017):
    """
    Load all intercommunalities from directory for the years from start to end
    """
    log.info('Processing intercommunalities from %s (%s-%s)',
             directory, start, end)
    intercommunalities = Intercommunalities()
    for year in range(start, end + 1):
        open_sirens = intercommunalities.open_sirens
        filename = os.path.join(directory, '{0}.csv'.format(year))
        for intercommunality in load_intercommunalities_from(filename,
                                                             year,
                                                             towns):
            if intercommunality.siren in open_sirens:
                # This is either the same or an update
                intercommunalities.update(intercommunality, year)
            else:
                # This is a creation
                intercommunalities.upsert(intercommunality.create_on(year))
            open_sirens.discard(intercommunality.siren)

        # All remaining SIRENs are now obsolete intercommunalities
        for siren in open_sirens:
            intercommunalities.ends(siren, year - 1, END_REMOVED)
    return intercommunalities


def attach_town(intercommunality, insee, validity, towns):
    try:
        intercommunality.towns.add(towns.get_current(insee, validity).id)
    except:
        log.error('Failed for %s on %s@%s',
                  intercommunality.name, insee, validity.isoformat())
        intercommunality.missing_towns.add((insee, validity))


INTERCOMMUNALITY_FIELDS = (
    'id', 'siren', 'name', 'acronym',
    'kind', 'taxmodel', 'towns',
    'start_date', 'end_date', 'end_reason',
    'successors', 'ancestors',
    'population',
)


def write_intercommunalities_on(filename, intercommunalities,
                                at_date=None):
    """
    Write the `filename` with CSV formatted informations.

    With the generated file, you will be able to retrace the history of
    a given SIREN code with all performed actions as comments.

    Each intercommunality has an associated population,
    sometimes computed from population of component towns.

    The `at_date` parameter allows you to only filter
    valid intercommunalities at that given date.
    """
    log.info('Writing intercommunalities file to %s', filename)
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile,
                                fieldnames=INTERCOMMUNALITY_FIELDS,
                                delimiter=',')
        writer.writeheader()

        if at_date:
            intercommunalities = intercommunalities.valid_at(at_date)
        else:
            intercommunalities = intercommunalities.values()

        for intercommunality in intercommunalities:
            writer.writerow({
                'id': intercommunality.id,
                'siren': intercommunality.siren,
                'name': intercommunality.name,
                'acronym': intercommunality.acronym,
                'kind': intercommunality.kind,
                'taxmodel': intercommunality.taxmodel,
                'start_date': intercommunality.start_date,
                'end_date': intercommunality.end_date,
                'end_reason': intercommunality.end_reason,
                'towns': ';'.join(intercommunality.towns),
                'successors': ';'.join(intercommunality.successors),
                'ancestors': ';'.join(intercommunality.ancestors),
                'population': intercommunality.population,
            })
