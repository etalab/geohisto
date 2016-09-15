"""Tests related to actions once towns and history_list are loaded."""
from datetime import datetime

from geohisto.actions import (
    do_renames, do_fusions, do_splits, do_fusions_to_new, do_deletions,
    do_obsoletes, do_change_county
)
from geohisto.constants import (
    RENAME_SIMPLE, RENAME_FUSION_LEADER, FUSION_FOLLOWER, SPLIT_LEADER,
    SPLIT_FOLLOWER, FUSION_TO_NEW_FOLLOWER, DELETION, OBSOLETE,
    CHANGE_COUNTY, START_DATE, END_DATE
)

from .test_towns_load import towns  # NOQA: fixtures.
from .test_history_load import history_list  # NOQA: fixtures.


def test_rename(towns, history_list):  # NOQA: fixtures.
    """Rename of the same town/id."""
    towns, history_list = do_renames(towns, history_list)
    neuville_s, neuville = towns.filter(depcom='10263')
    assert neuville_s.id == '102631942-01-01T00:00:002008-10-05T23:59:59'
    assert neuville_s.nccenr == 'Neuville-sur-Vannes'
    assert neuville_s.start_date == START_DATE
    assert neuville_s.end_date == datetime(2008, 10, 5, 23, 59, 59)
    assert neuville_s.modification == RENAME_SIMPLE
    assert neuville_s.successors == neuville.id
    assert neuville.id == '102632008-10-06T00:00:009999-12-31T23:59:59'
    assert neuville.nccenr == 'Neuville-sur-Vanne'
    assert neuville.start_date == datetime(2008, 10, 6, 0, 0, 0)
    assert neuville.end_date == END_DATE


def test_fusion(towns, history_list):  # NOQA: fixtures.
    """Fusion of 2 towns."""
    towns, history_list = do_fusions(towns, history_list)
    braguelogne, braguelogne_beauvoir = towns.filter(depcom='10058')
    beauvoir_sur_sarce = towns.filter(depcom='10036')[0]
    assert braguelogne.id == '100581942-01-01T00:00:001973-04-30T23:59:59'
    assert braguelogne.successors == braguelogne_beauvoir.id
    assert braguelogne.modification == RENAME_FUSION_LEADER
    assert braguelogne.nccenr == 'Bragelogne'
    assert (braguelogne_beauvoir.id
            == '100581973-05-01T00:00:009999-12-31T23:59:59')
    assert braguelogne_beauvoir.nccenr == 'Bragelogne-Beauvoir'
    assert (beauvoir_sur_sarce.id
            == '100361942-01-01T00:00:001973-04-30T23:59:59')
    assert beauvoir_sur_sarce.successors == braguelogne_beauvoir.id
    assert beauvoir_sur_sarce.modification == FUSION_FOLLOWER
    assert beauvoir_sur_sarce.nccenr == 'Beauvoir-sur-Sarce'


def test_fusion_then_split(towns, history_list):  # NOQA: fixtures.
    """Fusion then split of 2 towns."""
    towns, history_list = do_fusions(towns, history_list)
    framboisiere, framboisiere_saucelle = towns.filter(depcom='28159')
    saucelle = towns.filter(depcom='28368')[0]
    assert framboisiere.id == '281591942-01-01T00:00:001972-12-21T23:59:59'
    assert framboisiere.successors == framboisiere_saucelle.id
    assert framboisiere.modification == RENAME_FUSION_LEADER
    assert framboisiere.nccenr == 'Framboisière'
    assert (framboisiere_saucelle.id
            == '281591972-12-22T00:00:009999-12-31T23:59:59')
    assert framboisiere_saucelle.nccenr == 'Framboisière-la-Saucelle'
    assert saucelle.id == '283681942-01-01T00:00:001972-12-21T23:59:59'
    assert saucelle.successors == framboisiere_saucelle.id
    assert saucelle.modification == FUSION_FOLLOWER

    towns, history_list = do_splits(towns, history_list)
    framb, framb_saucelle, framb2 = towns.filter(depcom='28159')
    sauc, sauc2 = towns.filter(depcom='28368')
    assert framb_saucelle.id == '281591972-12-22T00:00:001986-12-31T23:59:59'
    assert framb_saucelle.successors == framb2.id + ';' + sauc2.id
    assert (framb_saucelle.modification
            == '{};{}'.format(SPLIT_LEADER, SPLIT_FOLLOWER))
    assert framb.id == '281591942-01-01T00:00:001972-12-21T23:59:59'
    assert framb.successors == framb_saucelle.id
    assert framb2.id == '281591987-01-01T00:00:009999-12-31T23:59:59'
    assert framb2.successors == ''
    assert sauc.id == '283681942-01-01T00:00:001972-12-21T23:59:59'
    assert sauc.successors == framb_saucelle.id
    assert sauc2.id == '283681987-01-01T00:00:009999-12-31T23:59:59'
    assert sauc2.successors == ''


def test_fusion_then_reinstatement_then_split(towns, history_list):  # NOQA: fixtures.
    """Fusion then split of 1 town, then split of another one."""
    towns, history_list = do_fusions(towns, history_list)
    towns, history_list = do_splits(towns, history_list)
    varenne, terre_natale, varenne2 = towns.filter(depcom='52504')
    champigny, champigny2 = towns.filter(depcom='52103')
    chezeau, chezeau2 = towns.filter(depcom='52124')
    assert varenne.id == '525041942-01-01T00:00:001972-07-31T23:59:59'
    assert terre_natale.id == '525041972-08-01T00:00:002011-12-31T23:59:59'
    assert varenne2.id == '525042012-01-01T00:00:009999-12-31T23:59:59'
    assert champigny.id == '521031942-01-01T00:00:001972-07-31T23:59:59'
    assert champigny2.id == '521031986-01-01T00:00:009999-12-31T23:59:59'
    assert chezeau.id == '521241942-01-01T00:00:001972-07-31T23:59:59'
    assert chezeau2.id == '521242012-01-01T00:00:009999-12-31T23:59:59'
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
    assert illtal.id == '682402016-01-01T00:00:009999-12-31T23:59:59'
    assert obedorf.id == '682401942-01-01T00:00:002015-12-31T23:59:59'
    assert grentzingen.id == '681081942-01-01T00:00:002015-12-31T23:59:59'
    assert henflingen.id == '681331942-01-01T00:00:002015-12-31T23:59:59'
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
    assert fragnes.id == '712041942-01-01T00:00:002015-12-31T23:59:59'
    assert loyere.id == '712651942-01-01T00:00:002015-12-31T23:59:59'
    assert fragnes_loyere.id == '712042016-01-01T00:00:009999-12-31T23:59:59'
    assert fragnes.successors == fragnes_loyere.id
    assert loyere.successors == fragnes_loyere.id
    assert fragnes.modification == FUSION_TO_NEW_FOLLOWER[0]
    assert loyere.modification == FUSION_TO_NEW_FOLLOWER[0]
    assert fragnes_loyere.nccenr == 'Fragnes-La Loyère'


def test_deletions(towns, history_list):  # NOQA: fixtures.
    """Deletion of a town."""
    towns, history_list = do_deletions(towns, history_list)
    creusy = towns.filter(depcom='45117')[0]
    assert creusy.id == '451171942-01-01T00:00:001964-12-31T23:59:59'
    assert creusy.successors == ''
    assert creusy.modification == DELETION
    assert creusy.nccenr == 'Creusy'


def test_obsoletes(towns, history_list):  # NOQA: fixtures.
    """Deletion of a town."""
    towns, history_list = do_obsoletes(towns, history_list)
    hauteville_lompnes = towns.filter(depcom='01459')[0]
    assert (hauteville_lompnes.id
            == '014591942-01-01T00:00:001942-07-31T23:59:59')
    assert (hauteville_lompnes.successors
            == '011851942-01-01T00:00:009999-12-31T23:59:59')
    assert hauteville_lompnes.modification == OBSOLETE
    assert hauteville_lompnes.nccenr == 'Hauteville-Lompnés'


def test_change_county(towns, history_list):  # NOQA: fixtures.
    """The town has changed from one county to another."""
    towns, history_list = do_change_county(towns, history_list)
    old_afa = towns.filter(depcom='20001')[0]
    new_afa = towns.filter(depcom='2A001')[0]
    assert old_afa.id == '200011942-01-01T00:00:001975-12-31T23:59:59'
    assert new_afa.id == '2A0011976-01-01T00:00:009999-12-31T23:59:59'
    assert old_afa.successors == '2A0011976-01-01T00:00:009999-12-31T23:59:59'
    assert old_afa.modification == CHANGE_COUNTY
