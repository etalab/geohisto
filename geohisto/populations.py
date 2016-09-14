from .utils import compute_population


def compute_populations(populations, towns):
    for _, town in towns:
        population_id = town.depcom + town.nccenr
        population = compute_population(
            populations, population_id, towns, town)
        towns += town._replace(population=population)
    return towns
