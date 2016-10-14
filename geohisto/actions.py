"""
Perform actions on towns given the modifications' types.

The modifications come from the history of changes.
"""

from functools import partial

from .constants import (
    SEPARATOR, DELTA, END_DATETIME, START_DATE, START_DATETIME,
    CHANGE_NAME, CHANGE_NAME_FUSION, CHANGE_NAME_CREATION,
    CHANGE_NAME_REINSTATEMENT,
    CREATION, REINSTATEMENT, SPLITING,
    DELETION_PARTITION, DELETION_FUSION,
    CREATION_NOT_DELEGATED, CREATION_NOT_DELEGATED_POLE,
    FUSION_ASSOCIATION_ASSOCIATED, CREATION_DELEGATED,
    CREATION_DELEGATED_POLE,
    CHANGE_COUNTY,
    OBSOLETE
)


def change_name(towns, record):
    current_town = towns.get_current(record.depcom, record.eff)

    new_town = current_town.generate(**{
        'id': current_town.depcom + SEPARATOR + record.effdate.isoformat(),
        'start_datetime': record.eff,
        'end_datetime': END_DATETIME,
        # `nccenr` changes on fusions.
        'nccenr': record.nccoff or current_town.nccenr,
        'successors': '',
    })
    towns.create(new_town)

    old_town = current_town.generate(**{
        'nccenr': record.nccanc,
        'end_datetime': record.eff - DELTA,
        'modification': record.mod
    })
    old_town = old_town.add_successor(new_town.id)
    towns.update(old_town, new_town)


def creation(towns, record, keep_current=False):
    current_town = towns.get_current(record.depcom, record.eff)

    new_town = current_town.generate(**{
        'id': current_town.depcom + SEPARATOR + record.effdate.isoformat(),
        'start_datetime': record.eff,
        'end_datetime': END_DATETIME,
        # `nccenr` changes on fusions.
        'nccenr': record.nccoff or current_town.nccenr,
        'modification': record.mod,
        'successors': '',
    })
    # It happens with `Pont-d'Ouilly` for instance.
    if new_town.id not in towns:
        towns.create(new_town, current_town)

    # Do not delete the initial town if all creations are not performed.
    if record.nbcom and record.nbcom != record.rangcom:
        return

    if (new_town.id != current_town.id
            and (new_town.nccenr == current_town.nccenr or not keep_current)):
        towns.delete(current_town)


def reinstatement(towns, record):
    current_town = towns.get_current(record.depcom, record.eff)

    id = current_town.depcom + SEPARATOR + record.effdate.isoformat()
    # It happens with `Avanchers-Valmorel` for instance
    # where a change name is performed at the same date.
    if id in towns:
        return

    new_town = current_town.generate(**{
        'id': id,
        'start_datetime': record.eff,
        'end_datetime': END_DATETIME,
        'nccenr': record.nccoff,
        'successors': '',
        'modification': 0
    })
    towns.create(new_town)#, current_town)

    old_town = current_town.generate(**{
        'nccenr': record.nccanc or record.nccoff,
        'end_datetime': min(current_town.end_datetime, record.eff - DELTA),
        'modification': record.mod
    })
    old_town = old_town.add_successor(new_town.id)
    towns.update(old_town)


def spliting(towns, record):
    current_town = towns.get_current(record.depcom, record.eff)

    current_town = current_town.generate(**{
        'modification': record.mod
    })
    towns.update(current_town)


def deletion(towns, record):
    current_town = towns.get_current(record.depcom, record.eff)

    end_datetime = record.eff - DELTA

    # It happens with `Lamarche-en-Woëvre` for instance
    # because the reinstatement is at the same date of the (re)fusion,
    # so we set the end_date just after the start_date exceptionnally.
    if current_town.start_datetime == record.eff:
        end_datetime = record.eff + DELTA

    old_town = current_town.generate(**{
        'nccenr': record.nccoff,
        'end_datetime': end_datetime,
        'modification': record.mod
    })
    successor = towns.get_current(record.comech, record.eff)
    old_town = old_town.add_successor(successor.id)
    towns.update(old_town)


def creation_not_delegated(towns, record):
    current_town = towns.get_current(record.depcom, record.eff)

    # Create new town only if it doesn't exist yet
    # (same depcom, different name).
    if record.depcom == record.comech and current_town.nccenr != record.nccoff:
        new_town = current_town.generate(**{
            'id': current_town.depcom + SEPARATOR + record.effdate.isoformat(),
            'start_datetime': record.eff,
            'modification': CREATION_NOT_DELEGATED_POLE
        })
        old_town = new_town.add_successor(current_town.id)
        towns.create(new_town, current_town)

        old_town = current_town.generate(**{
            'nccenr': record.nccoff,
            'end_datetime': record.eff - DELTA,
            'modification': record.mod
        })
        old_town = old_town.add_successor(new_town.id)
        towns.update(old_town)
    else:
        successor = towns.get_current(record.comech, record.eff)
        old_town = current_town.generate(**{
            'end_datetime': record.eff - DELTA,
            'modification': record.mod
        })
        old_town = old_town.add_successor(successor.id)
        towns.update(old_town)


def change_county(towns, record):
    current_town = towns.get_current(record.depcom, record.eff)
    # We set the `end_datetime` explicitely for the particular case
    # of Blamécourt where the town as fusioned before changin county.
    new_town = current_town.generate(**{
        'id': current_town.depcom + SEPARATOR + record.effdate.isoformat(),
        'start_datetime': record.eff,
        'end_datetime': max(current_town.end_datetime, record.eff + DELTA),
    })
    towns.create(new_town)
    towns.delete(current_town)

    current_town = towns.get_current(record.depanc, record.eff)
    if current_town.valid_at(record.eff):
        old_town = current_town.generate(**{
            'end_datetime': record.eff - DELTA,
            'modification': record.mod
        })
        old_town = old_town.add_successor(new_town.id)
        towns.update(old_town)
    else:
        # This particular case happens when there are multiple county
        # changes, for instance with Châteaufort.
        old_town = current_town.generate(**{
            'id': current_town.depcom + SEPARATOR + START_DATE.isoformat(),
            'start_datetime': START_DATETIME,
            'end_datetime': record.eff - DELTA,
            'modification': record.mod
        })
        old_town = old_town.add_successor(new_town.id)
        towns.create(old_town)


def obsolete(towns, record):
    current_town = towns.get_current(record.depcom, record.eff)

    old_town = current_town.generate(**{
        'end_datetime': record.eff - DELTA,
        'modification': record.mod
    })
    towns.update(old_town)


actions = {
    CHANGE_NAME: change_name,
    CHANGE_NAME_FUSION: change_name,
    CHANGE_NAME_CREATION: creation,
    CHANGE_NAME_REINSTATEMENT: reinstatement,
    CREATION: creation,
    REINSTATEMENT: reinstatement,
    SPLITING: spliting,
    DELETION_PARTITION: deletion,
    DELETION_FUSION: deletion,
    CREATION_NOT_DELEGATED: creation_not_delegated,
    FUSION_ASSOCIATION_ASSOCIATED: deletion,
    CREATION_DELEGATED: deletion,
    CREATION_DELEGATED_POLE: partial(creation, keep_current=True),
    CHANGE_COUNTY: change_county,
    OBSOLETE: obsolete,
}


def compute(towns, history):
    for record in history:
        try:
            actions.get(record.mod, lambda a, b: a)(towns, record)
        except Exception as e:
            print(record)
            raise e
