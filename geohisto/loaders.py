import csv

from .actions import (
    simple_rename,
    fusion_leader, fusion_follower,
    split_leader, split_follower
)
from .constants import START_DATE, END_DATE
from .utils import (
    convert_date, convert_leg, compute_name, compute_population,
    has_been_hard_renamed, add_same_ancestor, add_fusion_ancestor,
    has_been_renamed, add_ancestor, has_ancestor, has_changed_county,
    add_neighbor, has_been_restablished, has_been_deleted, restablish_town,
    delete_town, has_errored_numerotation, mark_as_errored, has_absorbed,
    add_absorbed_town
)


def load_towns(towns, filename='sources/france2016.txt'):
    """
    Load all towns from `filename` into a `towns` table.

    Warning: that file contains outdated towns but NOT renamed ones.
    """
    with open(filename, encoding='cp1252') as file:
        for line in csv.DictReader(file, delimiter='\t'):
            actual = int(line['ACTUAL'])
            if actual == 9:  # Cantonal fraction.
                continue  # Skip for the moment.
            town = {
                'actual': actual,
                'modification': 0,
                'successors': '',
                'start_date': START_DATE.isoformat(),
                'end_date': END_DATE.isoformat(),
                'dep': line['DEP'],
                'com': line['COM'],
                'nccenr': line['NCCENR'],
            }
            towns.insert(town)


def load_history(towns, filename='sources/historiq2016.txt'):
    """
    Compute successors for each `towns` given actions (renames, etc.).

    We are looping over the `filename` to detect renaming and merging
    actions within the past, enriching the given town with dates
    of these events and keys of ascendants.
    """
    with open(filename, encoding='cp1252') as file:
        for history in csv.DictReader(file, delimiter='\t'):
            history['eff'] = convert_date(history['EFF'])
            modification_type = history['mod'] = int(history['MOD'])
            if modification_type == 100:
                simple_rename(towns, history)
            elif modification_type == 110:
                fusion_leader(towns, history)
            elif modification_type == 330:
                fusion_follower(towns, history)
            elif modification_type == 120:
                split_leader(towns, history)
            elif modification_type == 210:
                split_follower(towns, history)

            # elif has_been_renamed(modification_type):
            #     if history['NCCOFF'] != town['nccenr']:
            #         town = towns.find_one(dep=history['DEP'],
            #                               com=history['COM'])
            #         add_fusion_ancestor(towns, town, history)
            # elif has_been_restablished(modification_type):
            #     town = towns.find_one(dep=history['DEP'], com=history['COM'])
            #     restablish_town(towns, town, history)
            # elif has_absorbed(town, history):
            #     add_absorbed_town(town, towns, history)
            # elif has_ancestor(town, towns, history):
            #     add_ancestor(town, towns, history)
            # elif has_changed_county(town, towns, history):
            #     add_neighbor(town, towns, history)
            # elif has_been_deleted(town, history):
            #     delete_town(town, history)
            # elif has_errored_numerotation(town, history):
            #     mark_as_errored(town)
