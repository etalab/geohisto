def compute_parents(counties, towns):
    """Update the parents for each town."""
    for _, town in towns.items():
        dep = town.depcom[:2]
        if dep == '97':  # DROM have 3-digits codes.
            dep = town.depcom[:3]
        parents = ';'.join(county['id'] for county in counties[dep])
        town = town.set_parents(parents)
        towns.upsert(town)
    return towns
