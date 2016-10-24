def compute_population(populations, population_id,
                       towns, town=None, key='metropole'):
    """
    Retrieve the population from `populations` dict cast as an integer.

    Fallback on `arrondissements` and `dom` if no population is found.
    Finally, a population of `0` is added for listed dead towns.
    In case of unknown population the value `NULL` is returned.

    If the `population_id` is missing and `town` is available, we try
    to compute the population based on ancestors (renames + merges).
    The `key` is useful for the recursivity of the function in order to
    explore different `populations` sub-dictionnaries.

    WARNING: you have to compute population AFTER computing ancestors.
    """
    # If the population is already available, return it.
    population = int(populations[key].get(population_id, 0))
    if population:
        return population
    elif town is None:
        return 'NULL'

    # Otherwise sum populations from ancestors towns.
    population = 0
    if town.ancestors:
        for ancestor_id in town.ancestors.split(';'):
            ancestor = towns.retrieve(ancestor_id)
            population_id = ancestor.depcom + ancestor.nccenr
            try:
                population += compute_population(
                    populations, population_id, towns)
            except TypeError:  # Returned population equals 'NULL'
                pass

    if not population:
        try:
            population += compute_population(
                populations, population_id, towns, key='arrondissements')
        except TypeError:  # Returned population equals 'NULL'
            pass
    if not population:
        try:
            population += compute_population(
                populations, population_id, towns, key='dom')
        except TypeError:  # Returned population equals 'NULL'
            pass
    if not population and population_id not in populations['mortes']:
        population = 'NULL'

    return population


def compute_populations(populations, towns):
    for _, town in towns.items():
        population_id = town.depcom + town.nccenr
        population = compute_population(
            populations, population_id, towns, town)
        town = town.set_population(population)
        towns.upsert(town)
    return towns
