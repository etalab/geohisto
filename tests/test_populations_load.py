import pytest

from geohisto.loaders import load_population_from


@pytest.fixture
def metropole_populations():
    return load_population_from('sources/population_metropole.csv')


@pytest.fixture
def arrondissements_populations():
    return load_population_from('sources/population_arrondissements.csv')


@pytest.fixture
def dom_populations():
    return load_population_from('sources/population_dom.csv')


@pytest.fixture
def mortes_populations():
    return load_population_from('sources/population_mortes.csv')


def test_metropole_load(metropole_populations):
    assert len(metropole_populations) == 36529


def test_arrondissements_load(arrondissements_populations):
    assert len(arrondissements_populations) == 45


def test_dom_load(dom_populations):
    assert len(dom_populations) == 113


def test_mortes_load(mortes_populations):
    assert len(mortes_populations) == 6
