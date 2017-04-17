from geohisto.loaders import load_population_from


def test_metropole_load():
    metropole_populations = load_population_from(
        'sources/population_metropole.csv')
    assert len(metropole_populations) == 36529


def test_arrondissements_load():
    arrondissements_populations = load_population_from(
        'sources/population_arrondissements.csv')
    assert len(arrondissements_populations) == 45


def test_dom_load():
    dom_populations = load_population_from('sources/population_dom.csv')
    assert len(dom_populations) == 112


def test_mortes_load():
    mortes_populations = load_population_from('sources/population_mortes.csv')
    assert len(mortes_populations) == 6
