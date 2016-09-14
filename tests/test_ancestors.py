"""Tests related to ancestors and populations."""
from geohisto.actions import do_all_actions
from geohisto.utils import compute_ancestors
from geohisto.populations import compute_populations

from .test_populations_load import (
    metropole_populations, arrondissements_populations, dom_populations,
    mortes_populations
)  # NOQA: fixtures.
from .test_towns_load import towns  # NOQA: fixtures.
from .test_history_load import history_list  # NOQA: fixtures.


def test_ancestors(towns, history_list):  # NOQA: fixtures.
    """Equivalent to the reverse of a successor relation."""
    towns, history_list = do_all_actions(towns, history_list)
    towns = compute_ancestors(towns)
    braguelogne, braguelogne_beauvoir = towns.filter(depcom='10058')
    beauvoir_sur_sarce = towns.filter(depcom='10036')[0]
    assert braguelogne.successors == braguelogne_beauvoir.id
    assert beauvoir_sur_sarce.successors == braguelogne_beauvoir.id
    assert (braguelogne_beauvoir.ancestors
            == ';'.join([braguelogne.id, beauvoir_sur_sarce.id]))


def test_with_ancestors_population(towns, history_list,   # NOQA: fixtures.
        metropole_populations,  # NOQA: fixtures.
        arrondissements_populations, dom_populations,   # NOQA: fixtures.
        mortes_populations):  # NOQA: fixtures.
    """Test populations once ancestor are set."""
    towns, history_list = do_all_actions(towns, history_list)
    towns = compute_ancestors(towns)
    populations = {
        'metropole': metropole_populations,
        'arrondissements': arrondissements_populations,
        'dom': dom_populations,
        'mortes': mortes_populations
    }
    towns = compute_populations(populations, towns)

    # We cannot compute old populations.
    braguelogne, braguelogne_beauvoir = towns.filter(depcom='10058')
    beauvoir_sur_sarce = towns.filter(depcom='10036')[0]
    assert braguelogne.population == 'NULL'
    assert beauvoir_sur_sarce.population == 'NULL'
    assert braguelogne_beauvoir.population == 249

    # But we can guess current population from fusions.
    saint_martin = towns.filter(depcom='89356')[0]
    saint_aubin, val_ocre = towns.filter(depcom='89334')
    assert saint_martin.population == 64
    assert saint_aubin.population == 517
    assert val_ocre.population == 581
