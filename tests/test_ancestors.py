"""Tests related to ancestors and populations."""


def test_ancestors(result):
    """Equivalent to the reverse of a successor relation."""
    bragelogne, bragelogne_beauvoir = result.filter(depcom='10058')
    beauvoir_sur_sarce = result.filter(depcom='10036')[0]
    assert bragelogne.successors == bragelogne_beauvoir.id
    assert beauvoir_sur_sarce.successors == bragelogne_beauvoir.id
    assert (bragelogne_beauvoir.ancestors
            == ';'.join([beauvoir_sur_sarce.id, bragelogne.id]))


def test_with_ancestors_population(result):
    """Test populations once ancestor are set."""
    # We cannot compute old populations.
    bragelogne, bragelogne_beauvoir = result.filter(depcom='10058')
    beauvoir_sur_sarce = result.filter(depcom='10036')[0]
    assert bragelogne.population == 'NULL'
    assert beauvoir_sur_sarce.population == 'NULL'
    assert bragelogne_beauvoir.population == 249

    # But we can guess current population from fusions.
    saint_martin = result.filter(depcom='89356')[0]
    saint_aubin, val_ocre = result.filter(depcom='89334')
    assert saint_martin.population == 64
    assert saint_aubin.population == 517
    assert val_ocre.population == 581
