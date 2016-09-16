"""Tests related to actions once towns and history_list are loaded."""
from datetime import date, datetime

from geohisto.actions import (
    do_renames, do_fusions, do_splits, do_fusions_to_new, do_deletions,
    do_obsoletes, do_change_county
)
from geohisto.constants import (
    RENAME_SIMPLE, RENAME_FUSION_LEADER, FUSION_FOLLOWER, SPLIT_LEADER,
    SPLIT_FOLLOWER, FUSION_TO_NEW_FOLLOWER, DELETION, OBSOLETE,
    CHANGE_COUNTY, START_DATE, END_DATE, START_DATETIME, END_DATETIME
)

from .test_towns_load import towns  # NOQA: fixtures.
from .test_history_load import history_list  # NOQA: fixtures.


def test_rename(towns, history_list):  # NOQA: fixtures.
    """Rename of the same town/id."""
    towns, history_list = do_renames(towns, history_list)
    neuville_s, neuville = towns.filter(depcom='10263')
    assert neuville_s.id == '10263@1942-01-01'
    assert neuville_s.nccenr == 'Neuville-sur-Vannes'
    assert neuville_s.start_date == START_DATE
    assert neuville_s.start_datetime == START_DATETIME
    assert neuville_s.end_date == date(2008, 10, 5)
    assert neuville_s.end_datetime == datetime(2008, 10, 5, 23, 59, 59)
    assert neuville_s.modification == RENAME_SIMPLE
    assert neuville_s.successors == neuville.id
    assert neuville.id == '10263@2008-10-06'
    assert neuville.nccenr == 'Neuville-sur-Vanne'
    assert neuville.start_date == date(2008, 10, 6)
    assert neuville.start_datetime == datetime(2008, 10, 6, 0, 0, 0)
    assert neuville.end_date == END_DATE
    assert neuville.end_datetime == END_DATETIME


def test_fusion(towns, history_list):  # NOQA: fixtures.
    """Fusion of 2 towns."""
    towns, history_list = do_fusions(towns, history_list)
    braguelogne, braguelogne_beauvoir = towns.filter(depcom='10058')
    beauvoir_sur_sarce = towns.filter(depcom='10036')[0]
    assert braguelogne.id == '10058@1942-01-01'
    assert braguelogne.successors == braguelogne_beauvoir.id
    assert braguelogne.modification == RENAME_FUSION_LEADER
    assert braguelogne.nccenr == 'Bragelogne'
    assert braguelogne_beauvoir.id == '10058@1973-05-01'
    assert braguelogne_beauvoir.nccenr == 'Bragelogne-Beauvoir'
    assert beauvoir_sur_sarce.id == '10036@1942-01-01'
    assert beauvoir_sur_sarce.successors == braguelogne_beauvoir.id
    assert beauvoir_sur_sarce.modification == FUSION_FOLLOWER
    assert beauvoir_sur_sarce.nccenr == 'Beauvoir-sur-Sarce'


def test_fusion_then_split(towns, history_list):  # NOQA: fixtures.
    """Fusion then split of 2 towns."""
    towns, history_list = do_fusions(towns, history_list)
    framboisiere, framboisiere_saucelle = towns.filter(depcom='28159')
    saucelle = towns.filter(depcom='28368')[0]
    assert framboisiere.id == '28159@1942-01-01'
    assert framboisiere.successors == framboisiere_saucelle.id
    assert framboisiere.modification == RENAME_FUSION_LEADER
    assert framboisiere.nccenr == 'Framboisière'
    assert framboisiere_saucelle.id == '28159@1972-12-22'
    assert framboisiere_saucelle.nccenr == 'Framboisière-la-Saucelle'
    assert saucelle.id == '28368@1942-01-01'
    assert saucelle.successors == framboisiere_saucelle.id
    assert saucelle.modification == FUSION_FOLLOWER

    towns, history_list = do_splits(towns, history_list)
    framb, framb_saucelle, framb2 = towns.filter(depcom='28159')
    sauc, sauc2 = towns.filter(depcom='28368')
    assert framb_saucelle.id == '28159@1972-12-22'
    assert framb_saucelle.successors == framb2.id + ';' + sauc2.id
    assert (framb_saucelle.modification
            == '{};{}'.format(SPLIT_LEADER, SPLIT_FOLLOWER))
    assert framb.id == '28159@1942-01-01'
    assert framb.successors == framb_saucelle.id
    assert framb2.id == '28159@1987-01-01'
    assert framb2.successors == ''
    assert sauc.id == '28368@1942-01-01'
    assert sauc.successors == framb_saucelle.id
    assert sauc2.id == '28368@1987-01-01'
    assert sauc2.successors == ''


def test_fusion_then_reinstatement_then_split(towns, history_list):  # NOQA: fixtures.
    """Fusion then split of 1 town, then split of another one."""
    towns, history_list = do_fusions(towns, history_list)
    towns, history_list = do_splits(towns, history_list)
    varenne, terre_natale, varenne2 = towns.filter(depcom='52504')
    champigny, champigny2 = towns.filter(depcom='52103')
    chezeau, chezeau2 = towns.filter(depcom='52124')
    assert varenne.id == '52504@1942-01-01'
    assert terre_natale.id == '52504@1972-08-01'
    assert varenne2.id == '52504@2012-01-01'
    assert champigny.id == '52103@1942-01-01'
    assert champigny2.id == '52103@1986-01-01'
    assert chezeau.id == '52124@1942-01-01'
    assert chezeau2.id == '52124@2012-01-01'
    assert varenne.successors == terre_natale.id
    assert champigny.successors == terre_natale.id
    assert chezeau.successors == terre_natale.id
    assert (terre_natale.successors
            == varenne2.id + ';' + champigny2.id + ';' + chezeau2.id)
    assert varenne.modification == RENAME_FUSION_LEADER
    assert (terre_natale.modification
            == '{};{};{}'.format(SPLIT_LEADER, SPLIT_FOLLOWER, SPLIT_FOLLOWER))
    assert champigny.modification == FUSION_FOLLOWER
    assert chezeau.modification == FUSION_FOLLOWER


def test_multiple_successors(towns, history_list):  # NOQA: fixtures.
    """Fusion then split of 3 towns."""
    towns, history_list = do_fusions(towns, history_list)
    towns, history_list = do_splits(towns, history_list)
    bourdenay, val_orvin, bourdenay2 = towns.filter(depcom='10054')
    successor1, successor2, successor3 = val_orvin.successors.split(';')
    assert bourdenay2.id == successor1
    bercenay, bercenay2 = towns.filter(depcom='10038')
    assert bercenay.successors == val_orvin.id
    assert bercenay2.id == successor2
    assert bercenay2.nccenr == 'Bercenay-le-Hayer'
    trancault, trancault2 = towns.filter(depcom='10383')
    assert trancault.successors == val_orvin.id
    assert trancault2.nccenr == 'Trancault'
    assert trancault2.id == successor3


def test_fusions_to_new_delegated(towns, history_list):  # NOQA: fixtures.
    """Fusion of 3 towns to create a new one."""
    towns, history_list = do_fusions_to_new(towns, history_list)
    obedorf, illtal = towns.filter(depcom='68240')
    grentzingen = towns.filter(depcom='68108')[0]
    henflingen = towns.filter(depcom='68133')[0]
    assert illtal.id == '68240@2016-01-01'
    assert illtal.start_datetime == datetime(2016, 1, 1, 0, 0, 0)
    assert illtal.end_datetime == END_DATETIME
    assert obedorf.id == '68240@1942-01-01'
    assert obedorf.start_datetime == START_DATETIME
    assert obedorf.end_datetime == datetime(2015, 12, 31, 23, 59, 59)
    assert grentzingen.id == '68108@1942-01-01'
    assert grentzingen.start_datetime == START_DATETIME
    assert grentzingen.end_datetime == datetime(2015, 12, 31, 23, 59, 59)
    assert henflingen.id == '68133@1942-01-01'
    assert henflingen.start_datetime == START_DATETIME
    assert henflingen.end_datetime == datetime(2015, 12, 31, 23, 59, 59)
    assert obedorf.successors == illtal.id
    assert grentzingen.successors == illtal.id
    assert henflingen.successors == illtal.id
    assert obedorf.modification == FUSION_TO_NEW_FOLLOWER[1]
    assert illtal.nccenr == 'Illtal'


def test_fusions_to_new_not_delegated(towns, history_list):  # NOQA: fixtures.
    """Absorption of a town."""
    towns, history_list = do_fusions_to_new(towns, history_list)
    fragnes, fragnes_loyere = towns.filter(depcom='71204')
    loyere = towns.filter(depcom='71265')[0]
    assert fragnes.id == '71204@1942-01-01'
    assert loyere.id == '71265@1942-01-01'
    assert fragnes_loyere.id == '71204@2016-01-01'
    assert fragnes.successors == fragnes_loyere.id
    assert loyere.successors == fragnes_loyere.id
    assert fragnes.modification == FUSION_TO_NEW_FOLLOWER[0]
    assert loyere.modification == FUSION_TO_NEW_FOLLOWER[0]
    assert fragnes_loyere.nccenr == 'Fragnes-La Loyère'


def test_deletions(towns, history_list):  # NOQA: fixtures.
    """Deletion of a town."""
    towns, history_list = do_deletions(towns, history_list)
    creusy = towns.filter(depcom='45117')[0]
    assert creusy.id == '45117@1942-01-01'
    assert creusy.successors == ''
    assert creusy.modification == DELETION
    assert creusy.nccenr == 'Creusy'


def test_obsoletes(towns, history_list):  # NOQA: fixtures.
    """Deletion of a town."""
    towns, history_list = do_obsoletes(towns, history_list)
    hauteville_lompnes = towns.filter(depcom='01459')[0]
    assert hauteville_lompnes.id == '01459@1942-01-01'
    assert hauteville_lompnes.successors == '01185@1942-01-01'
    assert hauteville_lompnes.modification == OBSOLETE
    assert hauteville_lompnes.nccenr == 'Hauteville-Lompnés'


def test_change_county(towns, history_list):  # NOQA: fixtures.
    """The town has changed from one county to another."""
    towns, history_list = do_change_county(towns, history_list)
    old_afa = towns.filter(depcom='20001')[0]
    new_afa = towns.filter(depcom='2A001')[0]
    assert old_afa.id == '20001@1942-01-01'
    assert new_afa.id == '2A001@1976-01-01'
    assert old_afa.successors == '2A001@1976-01-01'
    assert old_afa.modification == CHANGE_COUNTY
