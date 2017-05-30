import pytest

from geohisto.constants import (
    END_DATE, END_DATETIME, START_DATE, START_DATETIME
)
from geohisto.loaders import load_towns


@pytest.fixture
def loaded_towns():
    return load_towns()


def test_initial_load(loaded_towns):
    assert len(loaded_towns) == 39167


def test_contains_arles(loaded_towns):
    arles = loaded_towns.filter(depcom='13004')[0]
    assert arles.id == 'fr:commune:13004@1942-01-01'
    assert arles.dep == '13'
    assert arles.com == '004'
    assert arles.start_date == START_DATE
    assert arles.end_date == END_DATE
    assert arles.start_datetime == START_DATETIME
    assert arles.end_datetime == END_DATETIME
    assert arles.successors == ''
    assert arles.actual == 1
    assert arles.nccenr == 'Arles'


def test_convert_name(loaded_towns):
    la_batie_neuve = loaded_towns.filter(depcom='05017')[0]
    assert la_batie_neuve.nccenr == 'La Bâtie-Neuve'
    lescale = loaded_towns.filter(depcom='04079')[0]
    assert lescale.nccenr == "L'Escale"
