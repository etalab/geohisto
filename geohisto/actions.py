from .constants import END_DATE


def _get_town_from_history(towns, history):
    return towns.find_one(dep=history['DEP'], com=history['COM'])


def _get_ancestor_from_history(towns, town, history):
    ancestor = towns.find_one(dep=history['COMECH'][:2],
                              com=history['COMECH'][2:],
                              end_date=history['eff'].isoformat())
    if not ancestor:
        ancestor = towns.find_one(dep=history['COMECH'][:2],
                                  com=history['COMECH'][2:],
                                  start_date=town['end_date'])
    return ancestor


def _add_successor(current, depcom):
    successors = current['successors']
    if not successors:
        return depcom
    else:
        successors = successors.split(';')
        successors.append(depcom)
        successors.sort()  # Maintain order for tests.
        return ';'.join(successors)


def simple_rename(towns, history):
    town = _get_town_from_history(towns, history)

    # Update the original current record.
    original_start_date = town['start_date']
    town['start_date'] = history['eff'].isoformat()
    towns.update(town, 'id')

    # Create a new record based on the current one.
    town['start_date'] = original_start_date
    town['successors'] = _add_successor(town, town['dep'] + town['com'])
    town['modification'] = history['mod']
    town['end_date'] = history['eff'].isoformat()
    town['nccenr'] = history['NCCANC']
    del town['id']  # We cannot insert a new town with the same id.
    towns.insert(town)


def fusion_leader(towns, history):
    town = _get_town_from_history(towns, history)

    # Update the original current record.
    original_start_date = town['start_date']
    town['start_date'] = history['eff'].isoformat()
    towns.update(town, 'id')

    # Create a new record based on the old one.
    town['start_date'] = original_start_date
    town['end_date'] = history['eff'].isoformat()
    town['successors'] = _add_successor(town, town['dep'] + town['com'])
    town['modification'] = history['mod']
    town['nccenr'] = history['NCCANC']
    del town['id']  # We cannot insert a new town with the same id.
    towns.insert(town)


def fusion_follower(towns, history):
    town = _get_town_from_history(towns, history)

    # The original current record has already been updated in `fusion_leader`.

    # Update the record based on the old one.
    town['end_date'] = history['eff'].isoformat()
    town['successors'] = _add_successor(town, history['COMECH'])
    town['modification'] = history['mod']
    town['nccenr'] = history['NCCOFF']
    towns.update(town, 'id')


def split_leader(towns, history):
    town = _get_town_from_history(towns, history)

    # Update the original current record.
    town['nccenr'] = history['NCCOFF']
    original_start_date = town['start_date']
    town['start_date'] = history['eff'].isoformat()
    towns.update(town, 'id')

    # Create a new record based on the old one.
    town['start_date'] = original_start_date
    town['end_date'] = history['eff'].isoformat()
    town['successors'] = _add_successor(town, town['dep'] + town['com'])
    town['modification'] = history['mod']
    town['nccenr'] = history['NCCANC']
    del town['id']  # We cannot insert a new town with the same id.
    towns.insert(town)


def split_follower(towns, history):
    town = _get_town_from_history(towns, history)
    if town['com'] == '038':
        import ipdb; ipdb.set_trace()

    # Update the ancestor and its successors if available.
    ancestor = _get_ancestor_from_history(towns, town, history)
    if ancestor:
        ancestor['end_date'] = history['eff'].isoformat()
        ancestor['successors'] = _add_successor(ancestor,
                                                town['dep'] + town['com'])
        towns.update(ancestor, 'id')

    # Create a new record based on the old one.
    town['start_date'] = history['eff'].isoformat()
    town['end_date'] = END_DATE
    town['successors'] = ''
    town['modification'] = 0
    town['nccenr'] = history['NCCOFF']
    del town['id']  # We cannot insert a new town with the same id.
    towns.insert(town)
