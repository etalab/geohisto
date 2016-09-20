from .constants import (
    RENAME_FUSION_LEADER, FUSION_FOLLOWER, SPLIT_LEADER, SPLIT_FOLLOWER,
    RENAME_SIMPLE, FUSION_TO_NEW_LEADER, FUSION_TO_NEW_FOLLOWER, DELETION,
    OBSOLETE, CHANGE_COUNTY, DELTA, DELTADAY, SEPARATOR,
    ABSORPTION_LEADER, ABSORPTION_FOLLOWER
)


def do_renames(towns, history_list):
    for history in history_list.filter_by_mod(RENAME_SIMPLE):
        for town in towns.filter(depcom=history.depcom):
            # Create recent record based on the initial one.
            recent_town = town._replace(start_date=history.effdate)
            recent_town = recent_town._replace(start_datetime=history.eff)
            recent_town = recent_town._replace(id=(
                recent_town.depcom + SEPARATOR + history.effdate.isoformat()))
            towns += recent_town  # New id == create.

            # Update the initial old record (same id).
            old_town = town._replace(end_date=history.effdate - DELTADAY)
            old_town = old_town._replace(end_datetime=history.eff - DELTA)
            old_town = old_town._replace(successors=recent_town.id)
            old_town = old_town._replace(modification=history.mod)
            old_town = old_town._replace(nccenr=history.nccanc)
            towns += old_town  # Same id == update.

    return towns, history_list


def _do_fusions_leaders(towns, history_list):
    for history in history_list.filter_by_mod(RENAME_FUSION_LEADER):
        for town in towns.filter(depcom=history.depcom):
            # Create recent record based on the initial one.
            recent_town = town._replace(nccenr=history.nccoff)
            recent_town = recent_town._replace(start_date=history.effdate)
            recent_town = recent_town._replace(start_datetime=history.eff)
            recent_town = recent_town._replace(id=(
                recent_town.depcom + SEPARATOR + history.effdate.isoformat()))
            towns += recent_town  # New id == create.

            # Update the initial old record (same id).
            old_town = town._replace(end_date=history.effdate - DELTADAY)
            old_town = old_town._replace(end_datetime=history.eff - DELTA)
            old_town = old_town._replace(successors=recent_town.id)
            old_town = old_town._replace(modification=history.mod)
            old_town = old_town._replace(nccenr=history.nccanc)
            towns += old_town  # Same id == update.

    return towns, history_list


def _do_fusions_followers(towns, history_list):
    for history in history_list.filter_by_mod(FUSION_FOLLOWER):
        for town in towns.filter(depcom=history.depcom):
            # Recent record already created during leader's fusion.

            # However, we need to retrieve the successor previously updated.
            successor = towns.get((
                history.comech + SEPARATOR + history.effdate.isoformat()))

            # Update the initial old record (same id).
            old_town = town._replace(end_date=history.effdate - DELTADAY)
            old_town = old_town._replace(end_datetime=history.eff - DELTA)
            if successor is not None:  # TODO: see Towns model.
                old_town = old_town._replace(successors=successor.id)
            old_town = old_town._replace(modification=history.mod)
            old_town = old_town._replace(nccenr=history.nccoff)
            towns += old_town  # Same id == update.

    return towns, history_list


def do_fusions(towns, history_list):
    return _do_fusions_followers(*_do_fusions_leaders(towns, history_list))


def _do_splits_leaders(towns, history_list):
    for history in history_list.filter_by_mod(SPLIT_LEADER):
        town = towns.current(depcom=history.depcom)
        # Create recent record based on the initial one.
        recent_town = town._replace(nccenr=history.nccoff)
        recent_town = recent_town._replace(start_date=history.effdate)
        recent_town = recent_town._replace(start_datetime=history.eff)
        recent_town = recent_town._replace(id=(
            recent_town.depcom + SEPARATOR + history.effdate.isoformat()))
        towns += recent_town  # New id == create.

        # Update the initial old record (same id).
        original_town = town._replace(end_date=history.effdate - DELTADAY)
        original_town = original_town._replace(
            end_datetime=history.eff - DELTA)
        original_town = original_town._replace(successors=recent_town.id)
        original_town = original_town._replace(modification=history.mod)
        original_town = original_town._replace(nccenr=history.nccanc)
        towns += original_town  # Same id == update.

        # Update parents references accordingly.
        for parent in towns.parents(town.id):
            updated_parent = parent._replace(successors=original_town.id)
            towns += updated_parent  # Same id == update.

    return towns, history_list


def _do_splits_followers(towns, history_list):
    for history in history_list.filter_by_mod(SPLIT_FOLLOWER):
        for town in towns.filter(depcom=history.depcom):
            leader = towns.current(history.comech)
            parents = towns.parents(leader.id)
            if not parents:
                print('TODO: {leader} does not have parents, rel. 340'.format(
                      leader=leader))
                continue
            predecessor = parents[0]

            # Create new record based on the initial one.
            new_split = town._replace(id=(
                town.depcom + SEPARATOR + history.effdate.isoformat()))
            new_split = new_split._replace(start_date=history.effdate)
            new_split = new_split._replace(start_datetime=history.eff)
            new_split = new_split._replace(end_date=leader.end_date)
            new_split = new_split._replace(end_datetime=leader.end_datetime)
            new_split = new_split._replace(
                nccenr=history.nccanc or history.nccoff)
            new_split = new_split._replace(successors='')
            towns += new_split  # New id == create.

            # Update the predecessor.
            new_predecessor = predecessor._replace(
                successors=predecessor.successors + ';' + new_split.id)
            new_predecessor = new_predecessor._replace(
                modification=(
                    '{previous_modification};{new_modification}'
                ).format(previous_modification=predecessor.modification,
                         new_modification=history.mod))
            towns += new_predecessor  # Same id == update.

    return towns, history_list


def do_splits(towns, history_list):
    return _do_splits_followers(*_do_splits_leaders(towns, history_list))


def _do_fusions_to_new_leaders(towns, history_list):
    for history in history_list.filter_by_mods(FUSION_TO_NEW_LEADER):
        for town in towns.filter(depcom=history.depcom):
            # Create recent record based on the initial one.
            recent_town = town._replace(start_date=history.effdate)
            recent_town = recent_town._replace(start_datetime=history.eff)
            recent_town = recent_town._replace(id=(
                town.depcom + SEPARATOR + history.effdate.isoformat()))
            towns += recent_town  # New id == create.

    return towns, history_list


def _do_fusions_to_new_followers(towns, history_list):
    for history in history_list.filter_by_mods(FUSION_TO_NEW_FOLLOWER):
        for town in towns.filter(depcom=history.depcom):
            # Recent record already created during leader's fusion.

            # Skip existing new town.
            if history.eff == town.start_datetime:
                continue

            # However, we need to retrieve the successor previously updated.
            successor = towns.get((
                history.comech + SEPARATOR + history.effdate.isoformat()))

            # Update old record based on the initial one.
            old_town = town._replace(end_date=history.effdate - DELTADAY)
            old_town = old_town._replace(end_datetime=history.eff - DELTA)
            if successor is not None:  # TODO: see Towns model.
                old_town = old_town._replace(successors=successor.id)
            old_town = old_town._replace(modification=history.mod)
            old_town = old_town._replace(nccenr=history.nccoff)
            towns += old_town  # Same id == update.

    return towns, history_list


def do_fusions_to_new(towns, history_list):
    return _do_fusions_to_new_followers(
        *_do_fusions_to_new_leaders(towns, history_list))


def do_deletions(towns, history_list):
    for history in history_list.filter_by_mod(DELETION):
        for town in towns.filter(depcom=history.depcom):
            # Skip deletion if we already recorded it.
            if town.modification == DELETION:
                continue

            # Update old record based on the initial one.
            old_town = town._replace(end_date=history.effdate - DELTADAY)
            old_town = old_town._replace(end_datetime=history.eff - DELTA)
            old_town = old_town._replace(modification=history.mod)
            towns += old_town  # Same id == update.

    return towns, history_list


def do_obsoletes(towns, history_list):
    for history in history_list.filter_by_mod(OBSOLETE):
        for town in towns.filter(depcom=history.depcom):
            successor = towns.filter(depcom=history.comech)[0]

            # Update old record based on the initial one.
            old_town = town._replace(end_date=history.effdate - DELTADAY)
            old_town = old_town._replace(end_datetime=history.eff - DELTA)
            old_town = old_town._replace(modification=history.mod)
            old_town = old_town._replace(successors=successor.id)
            towns += old_town  # Same id == update.

    return towns, history_list


def do_change_county(towns, history_list):
    for history in history_list.filter_by_mod(CHANGE_COUNTY):
        for town in towns.filter(depcom=history.depcom):

            # Create the recent record.
            recent_town = town._replace(start_date=history.effdate)
            recent_town = recent_town._replace(start_datetime=history.eff)
            recent_town = recent_town._replace(id=(
                town.depcom + SEPARATOR + history.effdate.isoformat()))
            towns += recent_town  # New id == create.

            # Delete the old one with an incorrect id.
            towns.remove(town)

            # Update the ancient record.
            town = towns.filter(depcom=history.depanc)[0]
            ancient_town = town._replace(end_date=history.effdate - DELTADAY)
            ancient_town = ancient_town._replace(
                end_datetime=history.eff - DELTA)
            ancient_town = ancient_town._replace(modification=history.mod)
            ancient_town = ancient_town._replace(successors=recent_town.id)
            towns += ancient_town  # Same id == update.

    return towns, history_list


def _do_absorptions_leaders(towns, history_list):
    for history in history_list.filter_by_mod(ABSORPTION_LEADER):
        for town in towns.filter(depcom=history.depcom):
            # Update the leader with the modification type only.
            recent_town = town._replace(modification=history.mod)
            towns += recent_town  # Same id == update.

    return towns, history_list


def _do_absorptions_followers(towns, history_list):
    for history in history_list.filter_by_mod(ABSORPTION_FOLLOWER):
        for town in towns.filter(depcom=history.depcom):
            # We need to retrieve the leader previously updated.
            successor = towns.filter(history.comech)[0]

            # Update old record based on the initial one.
            old_town = town._replace(end_date=history.effdate - DELTADAY)
            old_town = old_town._replace(end_datetime=history.eff - DELTA)
            old_town = old_town._replace(successors=successor.id)
            old_town = old_town._replace(modification=history.mod)
            old_town = old_town._replace(nccenr=history.nccoff)
            towns += old_town  # Same id == update.

    return towns, history_list


def do_absorptions(towns, history_list):
    return _do_absorptions_followers(
        *_do_absorptions_leaders(towns, history_list))


def do_all_actions(towns, history_list):
    """
    One method to rule them all.

    WARNING: order matters at least for county changes which must be
    executed at first to avoid messing up with ids.
    """
    towns, history_list = do_change_county(towns, history_list)
    towns, history_list = do_renames(towns, history_list)
    towns, history_list = do_fusions(towns, history_list)
    towns, history_list = do_splits(towns, history_list)
    towns, history_list = do_fusions_to_new(towns, history_list)
    towns, history_list = do_absorptions(towns, history_list)
    towns, history_list = do_deletions(towns, history_list)
    towns, history_list = do_obsoletes(towns, history_list)
    return towns, history_list
