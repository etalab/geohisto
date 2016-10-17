"""
Perform actions on towns given the modifications' types.

The modifications come from the history of changes.
"""
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
from .utils import in_case_of, ACTIONS


@in_case_of(CHANGE_NAME, CHANGE_NAME_FUSION)
def change_name(towns, record):
    current_town = towns.get_current(record.depcom, record.eff)

    new_town = current_town.generate(
        id=current_town.depcom + SEPARATOR + record.effdate.isoformat(),
        start_datetime=record.eff,
        end_datetime=END_DATETIME,
        # `nccenr` changes on fusions.
        nccenr=record.nccoff or current_town.nccenr,
        successors=''
    )
    towns.upsert(new_town)

    old_town = current_town.generate(
        nccenr=record.nccanc,
        end_datetime=record.eff - DELTA,
        modification=record.mod
    )
    old_town = old_town.add_successor(new_town.id)
    towns.upsert(old_town)
    towns.update_successors(old_town, to_town=new_town)


@in_case_of(CHANGE_NAME_CREATION, CREATION)
def creation(towns, record):
    current_town = towns.get_current(record.depcom, record.eff)

    new_town = current_town.generate(
        id=current_town.depcom + SEPARATOR + record.effdate.isoformat(),
        start_datetime=record.eff,
        end_datetime=END_DATETIME,
        # `nccenr` changes on fusions.
        nccenr=record.nccoff or current_town.nccenr,
        modification=record.mod,
        successors=''
    )
    # It happens with `Pont-d'Ouilly` for instance.
    is_already_registered = new_town.id in towns
    if not is_already_registered:
        towns.upsert(new_town)
        towns.update_successors(new_town, from_town=current_town)

    has_new_id = new_town.id != current_town.id
    if has_new_id:
        towns.delete(current_town)


# TODO: add a test dedicated to that case (see False for deletion)
@in_case_of(CREATION_DELEGATED_POLE)
def creation_delegated(towns, record):
    current_town = towns.get_current(record.depcom, record.eff)

    new_town = current_town.generate(
        id=current_town.depcom + SEPARATOR + record.effdate.isoformat(),
        start_datetime=record.eff,
        end_datetime=END_DATETIME,
        # `nccenr` changes on fusions.
        nccenr=record.nccoff or current_town.nccenr,
        modification=record.mod,
        successors=''
    )
    # It happens with `Pont-d'Ouilly` for instance.
    is_already_registered = new_town.id in towns
    if not is_already_registered:
        towns.upsert(new_town)
        towns.update_successors(new_town, from_town=current_town)

    # Do not delete the initial town if all creations are not performed.
    has_another_record = record.nbcom and record.nbcom != record.rangcom
    if has_another_record:
        return

    has_different_ids = new_town.id != current_town.id
    has_the_same_name = new_town.nccenr == current_town.nccenr
    if has_different_ids and has_the_same_name:
        towns.delete(current_town)


@in_case_of(CHANGE_NAME_REINSTATEMENT, REINSTATEMENT)
def reinstatement(towns, record):
    current_town = towns.get_current(record.depcom, record.eff)

    id = current_town.depcom + SEPARATOR + record.effdate.isoformat()
    # It happens with `Avanchers-Valmorel` for instance
    # where a change name is performed at the same date.
    is_already_registered = id in towns
    if is_already_registered:
        return

    new_town = current_town.generate(
        id=id,
        start_datetime=record.eff,
        end_datetime=END_DATETIME,
        nccenr=record.nccoff,
        successors='',
        modification=0
    )
    towns.upsert(new_town)

    old_town = current_town.generate(
        nccenr=record.nccanc or record.nccoff,
        end_datetime=min(current_town.end_datetime, record.eff - DELTA),
        modification=record.mod
    )
    old_town = old_town.add_successor(new_town.id)
    towns.upsert(old_town)


@in_case_of(SPLITING)
def spliting(towns, record):
    current_town = towns.get_current(record.depcom, record.eff)

    current_town = current_town.generate(
        modification=record.mod
    )
    towns.upsert(current_town)


@in_case_of(DELETION_PARTITION, DELETION_FUSION,
            FUSION_ASSOCIATION_ASSOCIATED, CREATION_DELEGATED)
def deletion(towns, record):
    current_town = towns.get_current(record.depcom, record.eff)

    end_datetime = record.eff - DELTA

    # It happens with `Lamarche-en-Woëvre` for instance
    # because the reinstatement is at the same date of the (re)fusion,
    # so we set the end_date just after the start_date exceptionnally.
    has_temporary_existence = current_town.start_datetime == record.eff
    if has_temporary_existence:
        end_datetime = record.eff + DELTA

    old_town = current_town.generate(
        nccenr=record.nccoff,
        end_datetime=end_datetime,
        modification=record.mod
    )
    successor = towns.get_current(record.comech, record.eff)
    old_town = old_town.add_successor(successor.id)
    towns.upsert(old_town)


@in_case_of(CREATION_NOT_DELEGATED)
def creation_not_delegated(towns, record):
    current_town = towns.get_current(record.depcom, record.eff)

    # Create new town only if it doesn't exist yet
    # (same depcom, different name).
    has_same_depcom = record.depcom == record.comech
    has_different_name = current_town.nccenr != record.nccoff
    if has_same_depcom and has_different_name:
        new_town = current_town.generate(
            id=current_town.depcom + SEPARATOR + record.effdate.isoformat(),
            start_datetime=record.eff,
            modification=CREATION_NOT_DELEGATED_POLE
        )
        old_town = new_town.add_successor(current_town.id)
        towns.upsert(new_town)
        towns.update_successors(new_town, from_town=current_town)

        old_town = current_town.generate(
            nccenr=record.nccoff,
            end_datetime=record.eff - DELTA,
            modification=record.mod
        )
        old_town = old_town.add_successor(new_town.id)
        towns.upsert(old_town)
    else:
        successor = towns.get_current(record.comech, record.eff)
        old_town = current_town.generate(
            end_datetime=record.eff - DELTA,
            modification=record.mod
        )
        old_town = old_town.add_successor(successor.id)
        towns.upsert(old_town)


@in_case_of(CHANGE_COUNTY)
def change_county(towns, record):
    current_town = towns.get_current(record.depcom, record.eff)
    # We set the `end_datetime` explicitely for the particular case
    # of Blamécourt where the town as fusioned before changin county.
    new_town = current_town.generate(
        id=current_town.depcom + SEPARATOR + record.effdate.isoformat(),
        start_datetime=record.eff,
        end_datetime=max(current_town.end_datetime, record.eff + DELTA)
    )
    towns.upsert(new_town)
    towns.delete(current_town)

    current_town = towns.get_current(record.depanc, record.eff)
    current_town_is_valid = current_town.valid_at(record.eff)
    if current_town_is_valid:
        old_town = current_town.generate(
            end_datetime=record.eff - DELTA,
            modification=record.mod
        )
        old_town = old_town.add_successor(new_town.id)
        towns.upsert(old_town)
    else:
        # This particular case happens when there are multiple county
        # changes, for instance with Châteaufort.
        old_town = current_town.generate(
            id=current_town.depcom + SEPARATOR + START_DATE.isoformat(),
            start_datetime=START_DATETIME,
            end_datetime=record.eff - DELTA,
            modification=record.mod
        )
        old_town = old_town.add_successor(new_town.id)
        towns.upsert(old_town)


@in_case_of(OBSOLETE)
def obsolete(towns, record):
    current_town = towns.get_current(record.depcom, record.eff)

    old_town = current_town.generate(
        end_datetime=record.eff - DELTA,
        modification=record.mod
    )
    towns.upsert(old_town)


def compute(towns, history):
    for record in history:
        try:
            ACTIONS.get(record.mod, lambda a, b: a)(towns, record)
        except Exception as e:
            print(record)
            raise e
