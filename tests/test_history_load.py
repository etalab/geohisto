import dataset
import pytest

from geohisto.loaders import load_towns, load_history


@pytest.fixture(scope='module')
def towns():
    with dataset.connect('sqlite:///:memory:') as database:
        towns = database['towns']
        load_towns(towns)
        database.commit()
        load_history(towns)
        return towns


# def test_initial_load(towns):
#     assert len(towns) == 42893


def test_simple_rename(towns):
    neuville_vannes = towns.find_one(nccenr='Neuville-sur-Vannes')
    assert neuville_vannes['dep'] == '10'
    assert neuville_vannes['com'] == '263'
    assert neuville_vannes['start_date'] == '1942-01-01'
    assert neuville_vannes['end_date'] == '2008-10-06'
    assert neuville_vannes['successors'] == '10263'
    assert neuville_vannes['modification'] == 100

    neuville_vanne = towns.find_one(nccenr='Neuville-sur-Vanne')
    assert neuville_vanne['dep'] == '10'
    assert neuville_vanne['com'] == '263'
    assert neuville_vanne['start_date'] == '2008-10-06'
    assert neuville_vanne['end_date'] == '2020-01-01'
    assert neuville_vanne['successors'] == ''
    assert neuville_vanne['modification'] == 0


def test_fusion_leader(towns):
    bragelogne = towns.find_one(nccenr='Bragelogne')
    assert bragelogne['dep'] == '10'
    assert bragelogne['com'] == '058'
    assert bragelogne['start_date'] == '1942-01-01'
    assert bragelogne['end_date'] == '1973-05-01'
    assert bragelogne['successors'] == '10058'
    assert bragelogne['modification'] == 110

    bragelogne_beauvoir = towns.find_one(nccenr='Bragelogne-Beauvoir')
    assert bragelogne_beauvoir['dep'] == '10'
    assert bragelogne_beauvoir['com'] == '058'
    assert bragelogne_beauvoir['start_date'] == '1973-05-01'
    assert bragelogne_beauvoir['end_date'] == '2020-01-01'
    assert bragelogne_beauvoir['successors'] == ''
    assert bragelogne_beauvoir['modification'] == 0


def test_fusion_follower(towns):
    beauvoir = towns.find_one(nccenr='Beauvoir-sur-Sarce')
    assert beauvoir['dep'] == '10'
    assert beauvoir['com'] == '036'
    assert beauvoir['start_date'] == '1942-01-01'
    assert beauvoir['end_date'] == '1973-05-01'
    assert beauvoir['successors'] == '10058'
    assert beauvoir['modification'] == 330

    bragelogne_beauvoir = towns.find_one(nccenr='Bragelogne-Beauvoir')
    assert bragelogne_beauvoir['dep'] == '10'
    assert bragelogne_beauvoir['com'] == '058'
    assert bragelogne_beauvoir['start_date'] == '1973-05-01'
    assert bragelogne_beauvoir['end_date'] == '2020-01-01'
    assert bragelogne_beauvoir['successors'] == ''
    assert bragelogne_beauvoir['modification'] == 0


def test_split_leader(towns):
    framboisiere = towns.find_one(nccenr='Framboisière',
                                  start_date='1942-01-01')
    assert framboisiere['dep'] == '28'
    assert framboisiere['com'] == '159'
    assert framboisiere['start_date'] == '1942-01-01'
    assert framboisiere['end_date'] == '1972-12-22'
    assert framboisiere['successors'] == '28159'
    assert framboisiere['modification'] == 110

    framboisiere_saucelle = towns.find_one(nccenr='Framboisière-la-Saucelle')
    assert framboisiere_saucelle['dep'] == '28'
    assert framboisiere_saucelle['com'] == '159'
    assert framboisiere_saucelle['start_date'] == '1972-12-22'
    assert framboisiere_saucelle['end_date'] == '1987-01-01'
    assert framboisiere_saucelle['successors'] == '28159;28368'
    assert framboisiere_saucelle['modification'] == 120

    new_framboisiere = towns.find_one(nccenr='Framboisière',
                                      start_date='1987-01-01')
    assert new_framboisiere['dep'] == '28'
    assert new_framboisiere['com'] == '159'
    assert new_framboisiere['start_date'] == '1987-01-01'
    assert new_framboisiere['end_date'] == '2020-01-01'
    assert new_framboisiere['successors'] == ''
    assert new_framboisiere['modification'] == 0


def test_split_follower(towns):
    saucelle = towns.find_one(nccenr='Saucelle', start_date='1942-01-01')
    assert saucelle['dep'] == '28'
    assert saucelle['com'] == '368'
    assert saucelle['start_date'] == '1942-01-01'
    assert saucelle['end_date'] == '1972-12-22'
    assert saucelle['successors'] == '28159'
    assert saucelle['modification'] == 330

    framboisiere_saucelle = towns.find_one(nccenr='Framboisière-la-Saucelle')
    assert framboisiere_saucelle['dep'] == '28'
    assert framboisiere_saucelle['com'] == '159'
    assert framboisiere_saucelle['start_date'] == '1972-12-22'
    assert framboisiere_saucelle['end_date'] == '1987-01-01'
    assert framboisiere_saucelle['successors'] == '28159;28368'
    assert framboisiere_saucelle['modification'] == 120

    new_saucelle = towns.find_one(nccenr='Saucelle', start_date='1987-01-01')
    assert new_saucelle['dep'] == '28'
    assert new_saucelle['com'] == '368'
    assert new_saucelle['start_date'] == '1987-01-01'
    assert new_saucelle['end_date'] == '2020-01-01'
    assert new_saucelle['successors'] == ''
    assert new_saucelle['modification'] == 0


def test_multiple_fusions_and_splits(towns):
    bourdenay = towns.find_one(nccenr='Bourdenay', start_date='1942-01-01')
    assert bourdenay['dep'] == '10'
    assert bourdenay['com'] == '054'
    assert bourdenay['start_date'] == '1942-01-01'
    assert bourdenay['end_date'] == '1973-01-01'
    assert bourdenay['successors'] == '10054'
    assert bourdenay['modification'] == 110

    val_dorvin = towns.find_one(nccenr='Val-d\'Orvin')
    assert val_dorvin['dep'] == '10'
    assert val_dorvin['com'] == '054'
    assert val_dorvin['start_date'] == '1973-01-01'
    assert val_dorvin['end_date'] == '2000-01-01'
    assert val_dorvin['successors'] == '10038;10054;10383'
    assert bourdenay['modification'] == 120

    new_bourdenay = towns.find_one(nccenr='Bourdenay', start_date='2000-01-01')
    assert new_bourdenay['dep'] == '10'
    assert new_bourdenay['com'] == '054'
    assert new_bourdenay['start_date'] == '2000-01-01'
    assert new_bourdenay['end_date'] == '2020-01-01'
    assert new_bourdenay['successors'] == ''
