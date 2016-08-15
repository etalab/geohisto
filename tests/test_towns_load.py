import dataset
import pytest

from geohisto.loaders import load_towns


@pytest.fixture(scope='module')
def towns():
    with dataset.connect('sqlite:///:memory:') as database:
        towns = database['towns']
        load_towns(towns)
        database.commit()
        return towns


def test_initial_load(towns):
    assert len(towns) == 39166


def test_contains_arles(towns):
    arles = towns.find_one(nccenr='Arles')
    assert arles['dep'] == '13'
    assert arles['com'] == '004'
    assert arles['start_date'] == '1942-01-01'
    assert arles['end_date'] == '2020-01-01'
    assert arles['successors'] == ''
    assert arles['actual'] == 1
