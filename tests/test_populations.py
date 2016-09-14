from geohisto.populations import compute_populations

from .test_populations_load import (
    metropole_populations, arrondissements_populations, dom_populations,
    mortes_populations
)  # NOQA: fixtures.
from .test_towns_load import towns  # NOQA: fixtures.
from .test_history_load import history_list  # NOQA: fixtures.


def test_metropole_population(towns, metropole_populations,  # NOQA: fixtures.
        arrondissements_populations, dom_populations,   # NOQA: fixtures.
        mortes_populations):  # NOQA: fixtures.
    populations = {
        'metropole': metropole_populations,
        'arrondissements': arrondissements_populations,
        'dom': dom_populations,
        'mortes': mortes_populations
    }
    towns = compute_populations(populations, towns)
    arles = towns.filter(depcom='13004')[0]
    assert arles.population == 52566


def test_arrondissements_population(towns, metropole_populations,  # NOQA: fixtures.
        arrondissements_populations, dom_populations,   # NOQA: fixtures.
        mortes_populations):  # NOQA: fixtures.
    populations = {
        'metropole': metropole_populations,
        'arrondissements': arrondissements_populations,
        'dom': dom_populations,
        'mortes': mortes_populations
    }
    towns = compute_populations(populations, towns)
    marseille_12_arrondissement = towns.filter(depcom='13212')[0]
    assert marseille_12_arrondissement.population == 57908


def test_dom_population(towns, metropole_populations,  # NOQA: fixtures.
        arrondissements_populations, dom_populations,   # NOQA: fixtures.
        mortes_populations):  # NOQA: fixtures.
    populations = {
        'metropole': metropole_populations,
        'arrondissements': arrondissements_populations,
        'dom': dom_populations,
        'mortes': mortes_populations
    }
    towns = compute_populations(populations, towns)
    basse_terre = towns.filter(depcom='97105')[0]
    assert basse_terre.population == 11150


def test_mortes_population(towns, metropole_populations,  # NOQA: fixtures.
        arrondissements_populations, dom_populations,   # NOQA: fixtures.
        mortes_populations):  # NOQA: fixtures.
    populations = {
        'metropole': metropole_populations,
        'arrondissements': arrondissements_populations,
        'dom': dom_populations,
        'mortes': mortes_populations
    }
    towns = compute_populations(populations, towns)
    bezonvaux = towns.filter(depcom='55050')[0]
    assert bezonvaux.population == 0
