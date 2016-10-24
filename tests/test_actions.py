"""
Tests related to actions performed on towns given the history.

All fixtures are extracted from real cases located in france2016
and historiq2016 files.
"""
from datetime import date, datetime

from geohisto.actions import compute
from geohisto.constants import (
    START_DATE, END_DATE, START_DATETIME, END_DATETIME,
    CHANGE_NAME, CHANGE_NAME_FUSION, CHANGE_NAME_CREATION,
    CHANGE_NAME_REINSTATEMENT,
    CREATION, REINSTATEMENT, SPLITING,
    DELETION_PARTITION, DELETION_FUSION, FUSION_ABSORPTION,
    CREATION_NOT_DELEGATED, CREATION_NOT_DELEGATED_POLE,
    FUSION_ASSOCIATION_ASSOCIATED, CREATION_DELEGATED,
    CREATION_DELEGATED_POLE,
    CHANGE_COUNTY,
    OBSOLETE
)
from .factories import towns_factory, town_factory, record_factory


def test_change_name():
    """Change name of the same town (id)."""
    neuville_town = town_factory(
        dep='10', com='263', nccenr='Neuville-sur-Vanne')
    towns = towns_factory(neuville_town)
    change_name_record = record_factory(
        dep='10', com='263', mod=CHANGE_NAME, effdate=date(2008, 10, 6),
        nccoff='Neuville-sur-Vanne', nccanc='Neuville-sur-Vannes')
    history = [change_name_record]
    compute(towns, history)
    neuville_s, neuville = towns.filter(depcom='10263')
    assert neuville_s.id == '10263@1942-01-01'
    assert neuville_s.nccenr == 'Neuville-sur-Vannes'
    assert neuville_s.start_date == START_DATE
    assert neuville_s.start_datetime == START_DATETIME
    assert neuville_s.end_date == date(2008, 10, 5)
    assert neuville_s.end_datetime == datetime(2008, 10, 5, 23, 59, 59, 999999)
    assert neuville_s.modification == CHANGE_NAME
    assert neuville_s.successors == neuville.id
    assert neuville.id == '10263@2008-10-06'
    assert neuville.nccenr == 'Neuville-sur-Vanne'
    assert neuville.start_date == date(2008, 10, 6)
    assert neuville.start_datetime == datetime(2008, 10, 6, 0, 0, 0)
    assert neuville.end_date == END_DATE
    assert neuville.end_datetime == END_DATETIME


def test_change_name_many():
    """Change name of the same town (id), three times."""
    chalon_champagne_town = town_factory(
        dep='51', com='108', nccenr='Châlons-en-Champagne')
    towns = towns_factory(chalon_champagne_town)
    change_name_record1 = record_factory(
        dep='51', com='108', mod=CHANGE_NAME, effdate=date(1995, 11, 17),
        nccoff='Châlons-en-Champagne', nccanc='Châlons-sur-Marne')
    change_name_record2 = record_factory(
        dep='51', com='108', mod=CHANGE_NAME, effdate=date(1997, 5, 1),
        nccoff='Châlons-sur-Marne', nccanc='Châlons-en-Champagne')
    change_name_record3 = record_factory(
        dep='51', com='108', mod=CHANGE_NAME, effdate=date(1998, 1, 4),
        nccoff='Châlons-en-Champagne', nccanc='Châlons-sur-Marne')
    history = [change_name_record1, change_name_record2, change_name_record3]
    compute(towns, history)
    marne, champ, marne2, champ2 = towns.filter(depcom='51108')
    assert marne.id == '51108@1942-01-01'
    assert marne.nccenr == 'Châlons-sur-Marne'
    assert marne.start_date == START_DATE
    assert marne.start_datetime == START_DATETIME
    assert marne.end_date == date(1995, 11, 16)
    assert marne.end_datetime == datetime(1995, 11, 16, 23, 59, 59, 999999)
    assert marne.modification == CHANGE_NAME
    assert marne.successors == champ.id
    assert champ.id == '51108@1995-11-17'
    assert champ.nccenr == 'Châlons-en-Champagne'
    assert champ.start_date == date(1995, 11, 17)
    assert champ.start_datetime == datetime(1995, 11, 17, 0, 0, 0)
    assert champ.end_date == date(1997, 4, 30)
    assert champ.end_datetime == datetime(1997, 4, 30, 23, 59, 59, 999999)
    assert champ.successors == marne2.id
    assert marne2.id == '51108@1997-05-01'
    assert marne2.nccenr == 'Châlons-sur-Marne'
    assert marne2.start_date == date(1997, 5, 1)
    assert marne2.start_datetime == datetime(1997, 5, 1, 0, 0, 0)
    assert marne2.end_date == date(1998, 1, 3)
    assert marne2.end_datetime == datetime(1998, 1, 3, 23, 59, 59, 999999)
    assert marne2.modification == CHANGE_NAME
    assert marne2.successors == champ2.id
    assert champ2.id == '51108@1998-01-04'
    assert champ2.nccenr == 'Châlons-en-Champagne'
    assert champ2.start_date == date(1998, 1, 4)
    assert champ2.start_datetime == datetime(1998, 1, 4, 0, 0, 0)
    assert champ2.end_date == END_DATE
    assert champ2.end_datetime == END_DATETIME


def test_change_name_fusion():
    """Change name of a town during a fusion."""
    bragelogne_beavoir_town = town_factory(
        dep='10', com='058', nccenr='Bragelogne-Beauvoir')
    towns = towns_factory(bragelogne_beavoir_town)
    change_name_fusion_record = record_factory(
        dep='10', com='058', mod=CHANGE_NAME_FUSION, effdate=date(1973, 5, 1),
        nccoff='Bragelogne-Beauvoir', nccanc='Bragelogne')
    history = [change_name_fusion_record]
    compute(towns, history)
    braguelogne, braguelogne_beauvoir = towns.filter(depcom='10058')
    assert braguelogne.id == '10058@1942-01-01'
    assert braguelogne.successors == braguelogne_beauvoir.id
    assert braguelogne.modification == CHANGE_NAME_FUSION
    assert braguelogne.nccenr == 'Bragelogne'
    assert braguelogne_beauvoir.id == '10058@1973-05-01'
    assert braguelogne_beauvoir.nccenr == 'Bragelogne-Beauvoir'


def test_change_name_creation():
    """Change name of a town during a creation."""
    clefs_town = town_factory(dep='49', com='101', nccenr='Clefs')
    towns = towns_factory(clefs_town)
    change_name_creation_record = record_factory(
        dep='49', com='101', mod=CHANGE_NAME_CREATION,
        effdate=date(2016, 1, 1), nccoff='Clefs')
    history = [change_name_creation_record]
    compute(towns, history)
    clefs_list = towns.filter(depcom='49101')
    assert len(clefs_list) == 1
    clefs = clefs_list[0]
    assert clefs.id == '49101@2016-01-01'
    assert clefs.successors == ''
    assert clefs.modification == CHANGE_NAME_CREATION
    assert clefs.nccenr == 'Clefs'
    assert clefs.start_date == date(2016, 1, 1)
    assert clefs.start_datetime == datetime(2016, 1, 1, 0, 0, 0)
    assert clefs.end_date == END_DATE
    assert clefs.end_datetime == END_DATETIME


def test_change_name_reinstatement_after_fusion():
    """Change name of a town during a reinstatement following a fusion."""
    framboisiere_town = town_factory(
        dep='28', com='159', nccenr='Framboisière')
    saucelle_town = town_factory(
        dep='28', com='368', nccenr='Saucelle')
    towns = towns_factory(framboisiere_town, saucelle_town)
    change_name_fusion_record = record_factory(
        dep='28', com='159', mod=CHANGE_NAME_FUSION,
        effdate=date(1972, 12, 22),
        nccoff='Framboisière-la-Saucelle', nccanc='Framboisière')
    change_name_reinstatement_record = record_factory(
        dep='28', com='159', mod=CHANGE_NAME_REINSTATEMENT,
        effdate=date(1987, 1, 1),
        nccoff='Framboisière', nccanc='Framboisière-la-Saucelle')
    spliting_record = record_factory(
        dep='28', com='159', mod=SPLITING,
        effdate=date(1987, 1, 1),
        nccoff='Framboisière', comech='28368')
    history = [
        change_name_fusion_record, change_name_reinstatement_record,
        spliting_record
    ]
    compute(towns, history)
    framb, framb_saucelle, framb2 = towns.filter(depcom='28159')
    assert framb_saucelle.id == '28159@1972-12-22'
    assert framb_saucelle.successors == framb2.id
    assert framb_saucelle.modification == CHANGE_NAME_REINSTATEMENT
    assert framb.id == '28159@1942-01-01'
    assert framb.successors == framb_saucelle.id
    assert framb2.id == '28159@1987-01-01'
    assert framb2.successors == ''


def test_creation():
    """Creation of a new town."""
    curan_town = town_factory(dep='12', com='307', nccenr='Curan')
    towns = towns_factory(curan_town)
    creation_record = record_factory(
        dep='12', com='307', mod=CREATION,
        effdate=date(1952, 12, 3), nccoff='Curan')
    history = [creation_record]
    compute(towns, history)
    curan_list = towns.filter(depcom='12307')
    assert len(curan_list) == 1
    curan = curan_list[0]
    assert curan.id == '12307@1952-12-03'
    assert curan.successors == ''
    assert curan.modification == CREATION
    assert curan.nccenr == 'Curan'
    assert curan.start_date == date(1952, 12, 3)
    assert curan.start_datetime == datetime(1952, 12, 3, 0, 0, 0)
    assert curan.end_date == END_DATE
    assert curan.end_datetime == END_DATETIME


def test_reinstatement():
    """Reinstatement town."""
    brageac_town = town_factory(dep='15', com='024', nccenr='Brageac')
    towns = towns_factory(brageac_town)
    reinstatement_record = record_factory(
        dep='15', com='024', mod=REINSTATEMENT,
        effdate=date(1985, 10, 1), nccoff='Brageac')
    history = [reinstatement_record]
    compute(towns, history)
    old_brageac, new_brageac = towns.filter(depcom='15024')
    assert old_brageac.id == '15024@1942-01-01'
    assert old_brageac.successors == new_brageac.id
    assert old_brageac.modification == REINSTATEMENT
    assert old_brageac.nccenr == 'Brageac'
    assert old_brageac.start_date == START_DATE
    assert old_brageac.start_datetime == START_DATETIME
    assert old_brageac.end_date == date(1985, 9, 30)
    assert (old_brageac.end_datetime
            == datetime(1985, 9, 30, 23, 59, 59, 999999))
    assert new_brageac.id == '15024@1985-10-01'
    assert new_brageac.successors == ''
    assert new_brageac.modification == 0
    assert new_brageac.nccenr == 'Brageac'
    assert new_brageac.start_date == date(1985, 10, 1)
    assert new_brageac.start_datetime == datetime(1985, 10, 1, 0, 0, 0)
    assert new_brageac.end_date == END_DATE
    assert new_brageac.end_datetime == END_DATETIME


def test_fusion_then_reinstatement():
    """That case is important to verify that we don't mess with dates."""
    brageac_town = town_factory(dep='15', com='024', nccenr='Brageac')
    ally_town = town_factory(dep='15', com='003', nccenr='Ally')
    towns = towns_factory(brageac_town, ally_town)
    spliting_record = record_factory(
        dep='15', com='003', mod=SPLITING,
        effdate=date(1985, 10, 1), nccoff='Ally', comech='15024')
    fusion_record = record_factory(
        dep='15', com='024', mod=FUSION_ASSOCIATION_ASSOCIATED,
        effdate=date(1973, 1, 1), nccoff='Brageac', comech='15003')
    reinstatement_record = record_factory(
        dep='15', com='024', mod=REINSTATEMENT,
        effdate=date(1985, 10, 1), nccoff='Brageac', comech='15003')
    history = [spliting_record, fusion_record, reinstatement_record]
    compute(towns, history)
    ally_list = towns.filter(depcom='15003')
    assert len(ally_list) == 1
    ally = ally_list[0]
    old_brageac, new_brageac = towns.filter(depcom='15024')
    assert ally.successors == ''
    assert old_brageac.id == '15024@1942-01-01'
    assert old_brageac.successors == ally.id + ';' + new_brageac.id
    assert old_brageac.modification == REINSTATEMENT
    assert old_brageac.nccenr == 'Brageac'
    assert old_brageac.start_date == START_DATE
    assert old_brageac.start_datetime == START_DATETIME
    assert old_brageac.end_date == date(1972, 12, 31)
    assert (old_brageac.end_datetime
            == datetime(1972, 12, 31, 23, 59, 59, 999999))
    assert new_brageac.id == '15024@1985-10-01'
    assert new_brageac.successors == ''
    assert new_brageac.modification == 0
    assert new_brageac.nccenr == 'Brageac'
    assert new_brageac.start_date == date(1985, 10, 1)
    assert new_brageac.start_datetime == datetime(1985, 10, 1, 0, 0, 0)
    assert new_brageac.end_date == END_DATE
    assert new_brageac.end_datetime == END_DATETIME


def test_deletion_partition():
    """Deletion of an old town (partition)."""
    creusy_town = town_factory(dep='45', com='117', nccenr='Creusy')
    chevilly_town = town_factory(dep='45', com='093', nccenr='Chevilly')
    sougy_town = town_factory(dep='45', com='313', nccenr='Sougy')
    towns = towns_factory(creusy_town, chevilly_town, sougy_town)
    deletion_partition_record1 = record_factory(
        dep='45', com='117', mod=DELETION_PARTITION,
        effdate=date(1965, 1, 1), nccoff='Creusy', comech='45093')
    deletion_partition_record2 = record_factory(
        dep='45', com='117', mod=DELETION_PARTITION,
        effdate=date(1965, 1, 1), nccoff='Creusy', comech='45313')
    history = [deletion_partition_record1, deletion_partition_record2]
    compute(towns, history)
    creusy_list = towns.filter(depcom='45117')
    assert len(creusy_list) == 1
    creusy = creusy_list[0]
    assert creusy.id == '45117@1942-01-01'
    assert creusy.successors == '45093@1942-01-01;45313@1942-01-01'
    assert creusy.modification == DELETION_PARTITION
    assert creusy.nccenr == 'Creusy'
    assert creusy.start_date == START_DATE
    assert creusy.start_datetime == START_DATETIME
    assert creusy.end_date == date(1964, 12, 31)
    assert creusy.end_datetime == datetime(1964, 12, 31, 23, 59, 59, 999999)


def test_deletion_fusion():
    """Deletion of an old town (partition)."""
    eyvignes_town = town_factory(dep='24', com='169',
                                 nccenr='Eyvignes-et-Eybènes')
    salignac_town = town_factory(dep='24', com='516',
                                 nccenr='Salignac-Eyvigues')
    towns = towns_factory(eyvignes_town, salignac_town)
    deletion_fusion_record = record_factory(
        dep='24', com='169', mod=DELETION_FUSION,
        effdate=date(1965, 3, 1), nccoff='Eyvignes-et-Eybènes', comech='24516')
    history = [deletion_fusion_record]
    compute(towns, history)
    eyvignes_list = towns.filter(depcom='24169')
    assert len(eyvignes_list) == 1
    eyvignes = eyvignes_list[0]
    assert eyvignes.id == '24169@1942-01-01'
    assert eyvignes.successors == '24516@1942-01-01'
    assert eyvignes.modification == DELETION_FUSION
    assert eyvignes.nccenr == 'Eyvignes-et-Eybènes'
    assert eyvignes.start_date == START_DATE
    assert eyvignes.start_datetime == START_DATETIME
    assert eyvignes.end_date == date(1965, 2, 28)
    assert eyvignes.end_datetime == datetime(1965, 2, 28, 23, 59, 59, 999999)


def test_fusion_absorption():
    """Fusion of a town with absorption."""
    castilly_town = town_factory(dep='14', com='142', nccenr='Castilly')
    mestry_town = town_factory(dep='14', com='428', nccenr='Mestry')
    towns = towns_factory(castilly_town, mestry_town)
    fusion_absorption_record = record_factory(
        dep='14', com='142', mod=FUSION_ABSORPTION,
        effdate=date(1965, 2, 15), nccoff='Castilly', comech='14428')
    deletion_fusion_record = record_factory(
        dep='14', com='428', mod=DELETION_FUSION,
        effdate=date(1965, 2, 15), nccoff='Mestry', comech='14142')
    history = [fusion_absorption_record, deletion_fusion_record]
    compute(towns, history)
    castilly_list = towns.filter(depcom='14142')
    assert len(castilly_list) == 1
    castilly = castilly_list[0]
    assert castilly.id == '14142@1942-01-01'
    assert castilly.successors == ''
    assert castilly.modification == 0
    assert castilly.nccenr == 'Castilly'
    assert castilly.start_date == START_DATE
    assert castilly.start_datetime == START_DATETIME
    assert castilly.end_date == END_DATE
    assert castilly.end_datetime == END_DATETIME
    mestry_list = towns.filter(depcom='14428')
    assert len(mestry_list) == 1
    mestry = mestry_list[0]
    assert mestry.id == '14428@1942-01-01'
    assert mestry.successors == castilly.id
    assert mestry.modification == DELETION_FUSION
    assert mestry.nccenr == 'Mestry'
    assert mestry.start_date == START_DATE
    assert mestry.start_datetime == START_DATETIME
    assert mestry.end_date == date(1965, 2, 14)
    assert mestry.end_datetime == datetime(1965, 2, 14, 23, 59, 59, 999999)


def test_creation_not_delegated():
    """New town without delegate."""
    fragnes_loyere_town = town_factory(dep='71', com='204',
                                       nccenr='Fragnes-La Loyère')
    loyere_town = town_factory(dep='71', com='265', nccenr='Loyère')
    towns = towns_factory(fragnes_loyere_town, loyere_town)
    creation_not_delegated_record1 = record_factory(
        dep='71', com='204', mod=CREATION_NOT_DELEGATED,
        effdate=date(2016, 1, 1), nccoff='Fragnes', comech='71204')
    creation_not_delegated_pole_record1 = record_factory(
        dep='71', com='204', mod=CREATION_NOT_DELEGATED_POLE,
        effdate=date(2016, 1, 1), nccoff='Fragnes-La Loyère', comech='71204')
    creation_not_delegated_pole_record2 = record_factory(
        dep='71', com='204', mod=CREATION_NOT_DELEGATED_POLE,
        effdate=date(2016, 1, 1), nccoff='Fragnes-La Loyère', comech='71265')
    creation_not_delegated_record2 = record_factory(
        dep='71', com='265', mod=CREATION_NOT_DELEGATED,
        effdate=date(2016, 1, 1), nccoff='Loyère', comech='71204')
    history = [
        creation_not_delegated_record1, creation_not_delegated_pole_record1,
        creation_not_delegated_pole_record2, creation_not_delegated_record2
    ]
    compute(towns, history)
    fragnes, fragnes_loyere = towns.filter(depcom='71204')
    loyere = towns.filter(depcom='71265')[0]
    assert fragnes.id == '71204@1942-01-01'
    assert fragnes.modification == CREATION_NOT_DELEGATED
    assert fragnes.successors == fragnes_loyere.id
    assert fragnes.nccenr == 'Fragnes'
    assert fragnes.start_date == START_DATE
    assert fragnes.start_datetime == START_DATETIME
    assert fragnes.end_date == date(2015, 12, 31)
    assert fragnes.end_datetime == datetime(2015, 12, 31, 23, 59, 59, 999999)
    assert loyere.id == '71265@1942-01-01'
    assert loyere.modification == CREATION_NOT_DELEGATED
    assert loyere.successors == fragnes_loyere.id
    assert loyere.nccenr == 'Loyère'
    assert loyere.start_date == START_DATE
    assert loyere.start_datetime == START_DATETIME
    assert loyere.end_date == date(2015, 12, 31)
    assert loyere.end_datetime == datetime(2015, 12, 31, 23, 59, 59, 999999)
    assert fragnes_loyere.id == '71204@2016-01-01'
    assert fragnes_loyere.modification == CREATION_NOT_DELEGATED_POLE
    assert fragnes_loyere.successors == ''
    assert fragnes_loyere.nccenr == 'Fragnes-La Loyère'
    assert fragnes_loyere.start_date == date(2016, 1, 1)
    assert fragnes_loyere.start_datetime == datetime(2016, 1, 1, 0, 0, 0)
    assert fragnes_loyere.end_date == END_DATE
    assert fragnes_loyere.end_datetime == END_DATETIME


def test_fusion_association_associated():
    """Fusion-association: associated town."""
    falgueyrat_town = town_factory(dep='24', com='173', nccenr='Falgueyrat')
    plaisance_town = town_factory(dep='24', com='168', nccenr='Plaisance')
    towns = towns_factory(falgueyrat_town, plaisance_town)
    fusion_association_associated_record = record_factory(
        dep='24', com='173', mod=FUSION_ASSOCIATION_ASSOCIATED,
        effdate=date(1973, 1, 1), nccoff='Falgueyrat', comech='24168')
    history = [fusion_association_associated_record]
    compute(towns, history)
    falgueyrat_list = towns.filter(depcom='24173')
    assert len(falgueyrat_list) == 1
    falgueyrat = falgueyrat_list[0]
    assert falgueyrat.id == '24173@1942-01-01'
    assert falgueyrat.successors == '24168@1942-01-01'
    assert falgueyrat.modification == FUSION_ASSOCIATION_ASSOCIATED
    assert falgueyrat.nccenr == 'Falgueyrat'
    assert falgueyrat.start_date == START_DATE
    assert falgueyrat.start_datetime == START_DATETIME
    assert falgueyrat.end_date == date(1972, 12, 31)
    assert (falgueyrat.end_datetime
            == datetime(1972, 12, 31, 23, 59, 59, 999999))


def test_creation_delegated():
    """New town: delegated."""
    grentzingen_town = town_factory(dep='68', com='108', nccenr='Grentzingen')
    illtal_town = town_factory(dep='68', com='240', nccenr='Illtal')
    towns = towns_factory(grentzingen_town, illtal_town)
    creation_delegated_record = record_factory(
        dep='68', com='108', mod=CREATION_DELEGATED,
        effdate=date(2016, 1, 1), nccoff='Grentzingen', comech='68240')
    history = [creation_delegated_record]
    compute(towns, history)
    grentzingen_list = towns.filter(depcom='68108')
    assert len(grentzingen_list) == 1
    grentzingen = grentzingen_list[0]
    assert grentzingen.id == '68108@1942-01-01'
    assert grentzingen.successors == '68240@1942-01-01'
    assert grentzingen.modification == CREATION_DELEGATED
    assert grentzingen.nccenr == 'Grentzingen'
    assert grentzingen.start_date == START_DATE
    assert grentzingen.start_datetime == START_DATETIME
    assert grentzingen.end_date == date(2015, 12, 31)
    assert (grentzingen.end_datetime
            == datetime(2015, 12, 31, 23, 59, 59, 999999))


def test_creation_delegated_pole():
    """New town: delegated - pole."""
    grentzingen_town = town_factory(dep='68', com='108', nccenr='Grentzingen')
    henflingen_town = town_factory(dep='68', com='133', nccenr='Henflingen')
    illtal_town = town_factory(dep='68', com='240', nccenr='Illtal')
    towns = towns_factory(grentzingen_town, henflingen_town, illtal_town)
    creation_delegated_record = record_factory(
        dep='68', com='108', mod=CREATION_DELEGATED,
        effdate=date(2016, 1, 1), nccoff='Grentzingen', comech='68240')
    creation_delegated_pole_record1 = record_factory(
        dep='68', com='240', mod=CREATION_DELEGATED_POLE,
        effdate=date(2016, 1, 1), nccoff='Illtal', comech='68108',
        last=False)
    creation_delegated_pole_record2 = record_factory(
        dep='68', com='240', mod=CREATION_DELEGATED_POLE,
        effdate=date(2016, 1, 1), nccoff='Illtal', comech='68133',
        last=False)
    creation_delegated_pole_record3 = record_factory(
        dep='68', com='240', mod=CREATION_DELEGATED_POLE,
        effdate=date(2016, 1, 1), nccoff='Illtal', comech='68240',
        last=True)
    history = [
        creation_delegated_record, creation_delegated_pole_record1,
        creation_delegated_pole_record2, creation_delegated_pole_record3
    ]
    compute(towns, history)
    grentzingen_list = towns.filter(depcom='68108')
    assert len(grentzingen_list) == 1
    grentzingen = grentzingen_list[0]
    illtal_list = towns.filter(depcom='68240')
    assert len(illtal_list) == 1
    illtal = illtal_list[0]
    assert grentzingen.id == '68108@1942-01-01'
    assert grentzingen.successors == illtal.id
    assert grentzingen.modification == CREATION_DELEGATED
    assert grentzingen.nccenr == 'Grentzingen'
    assert grentzingen.start_date == START_DATE
    assert grentzingen.start_datetime == START_DATETIME
    assert grentzingen.end_date == date(2015, 12, 31)
    assert (grentzingen.end_datetime
            == datetime(2015, 12, 31, 23, 59, 59, 999999))
    assert illtal.id == '68240@2016-01-01'
    assert illtal.successors == ''
    assert illtal.modification == CREATION_DELEGATED_POLE
    assert illtal.nccenr == 'Illtal'
    assert illtal.start_date == date(2016, 1, 1)
    assert illtal.start_datetime == datetime(2016, 1, 1, 0, 0, 0)
    assert illtal.end_date == END_DATE
    assert illtal.end_datetime == END_DATETIME


def test_change_county():
    """Town changed county."""
    new_afa_town = town_factory(dep='2A', com='001', nccenr='Afa')
    old_afa_town = town_factory(dep='20', com='001', nccenr='Afa')
    towns = towns_factory(new_afa_town, old_afa_town)
    change_county_record = record_factory(
        dep='2A', com='001', mod=CHANGE_COUNTY,
        effdate=date(1976, 1, 1), nccoff='Afa', depanc='20001')
    history = [change_county_record]
    compute(towns, history)
    afa_list = towns.filter(depcom='2A001')
    assert len(afa_list) == 1
    afa = afa_list[0]
    assert afa.id == '2A001@1976-01-01'
    assert afa.successors == ''
    assert afa.modification == 0
    assert afa.nccenr == 'Afa'
    assert afa.start_date == date(1976, 1, 1)
    assert afa.start_datetime == datetime(1976, 1, 1, 0, 0, 0)
    assert afa.end_date == END_DATE
    assert afa.end_datetime == END_DATETIME
    old_afa_list = towns.filter(depcom='20001')
    assert len(old_afa_list) == 1
    old_afa = old_afa_list[0]
    assert old_afa.id == '20001@1942-01-01'
    assert old_afa.successors == '2A001@1976-01-01'
    assert old_afa.modification == CHANGE_COUNTY
    assert old_afa.nccenr == 'Afa'
    assert old_afa.start_date == START_DATE
    assert old_afa.start_datetime == START_DATETIME
    assert old_afa.end_date == date(1975, 12, 31)
    assert old_afa.end_datetime == datetime(1975, 12, 31, 23, 59, 59, 999999)


def test_change_county_twice():
    old_chateaufort_town = town_factory(dep='78', com='143',
                                        nccenr='Châteaufort')
    new_chateaufort_town = town_factory(dep='91', com='143',
                                        nccenr='Châteaufort')
    towns = towns_factory(new_chateaufort_town, old_chateaufort_town)
    change_county1_record = record_factory(
        dep='78', com='143', mod=CHANGE_COUNTY,
        effdate=date(1969, 11, 29), nccoff='Châteaufort', comech='91143')
    change_county2_record = record_factory(
        dep='91', com='143', mod=CHANGE_COUNTY,
        effdate=date(1968, 1, 1), nccoff='Châteaufort', depanc='78143')
    history = [change_county1_record, change_county2_record]
    compute(towns, history)
    old_chateaufort, chateaufort = towns.filter(depcom='78143')
    tmp_chateaufort_list = towns.filter(depcom='91143')
    assert len(tmp_chateaufort_list) == 1
    tmp_chateaufort = tmp_chateaufort_list[0]
    assert chateaufort.id == '78143@1969-11-29'
    assert chateaufort.successors == ''
    assert chateaufort.modification == 0
    assert chateaufort.nccenr == 'Châteaufort'
    assert chateaufort.start_date == date(1969, 11, 29)
    assert chateaufort.start_datetime == datetime(1969, 11, 29, 0, 0, 0)
    assert chateaufort.end_date == END_DATE
    assert chateaufort.end_datetime == END_DATETIME
    assert old_chateaufort.id == '78143@1942-01-01'
    assert old_chateaufort.successors == tmp_chateaufort.id
    assert old_chateaufort.modification == CHANGE_COUNTY
    assert old_chateaufort.nccenr == 'Châteaufort'
    assert old_chateaufort.start_date == START_DATE
    assert old_chateaufort.start_datetime == START_DATETIME
    assert old_chateaufort.end_date == date(1967, 12, 31)
    assert (old_chateaufort.end_datetime
            == datetime(1967, 12, 31, 23, 59, 59, 999999))
    assert tmp_chateaufort.id == '91143@1968-01-01'
    assert tmp_chateaufort.successors == chateaufort.id
    assert tmp_chateaufort.modification == CHANGE_COUNTY
    assert tmp_chateaufort.nccenr == 'Châteaufort'
    assert tmp_chateaufort.start_date == date(1968, 1, 1)
    assert tmp_chateaufort.start_datetime == datetime(1968, 1, 1, 0, 0, 0)
    assert tmp_chateaufort.end_date == date(1969, 11, 28)
    assert (tmp_chateaufort.end_datetime
            == datetime(1969, 11, 28, 23, 59, 59, 999999))


def test_fusion_then_change_county():
    """Town fusion then changed county."""
    old_magny_town = town_factory(dep='78', com='355', nccenr='Magny-en-Vexin')
    new_magny_town = town_factory(dep='95', com='355', nccenr='Magny-en-Vexin')
    old_blamecourt_town = town_factory(dep='78', com='065',
                                       nccenr='Blamécourt')
    new_blamecourt_town = town_factory(dep='95', com='065',
                                       nccenr='Blamécourt')
    towns = towns_factory(old_magny_town, new_magny_town,
                          new_blamecourt_town, old_blamecourt_town)
    # Warning: the depcom reference is at a date where 95065
    # and 95355 do not exist yet!
    fusion_record = record_factory(
        dep='95', com='065', mod=DELETION_FUSION,
        effdate=date(1965, 1, 9), nccoff='Blamécourt', comech='95355')
    change_county_record = record_factory(
        dep='95', com='065', mod=CHANGE_COUNTY,
        effdate=date(1968, 1, 1), nccoff='Blamécourt', depanc='78065')
    history = [fusion_record, change_county_record]
    compute(towns, history)
    blamecourt_list = towns.filter(depcom='95065')
    assert len(blamecourt_list) == 1
    blamecourt = blamecourt_list[0]
    assert blamecourt.id == '95065@1968-01-01'
    assert blamecourt.successors == towns.filter(depcom='95355')[0].id
    assert blamecourt.modification == DELETION_FUSION
    assert blamecourt.nccenr == 'Blamécourt'
    assert blamecourt.start_date == date(1968, 1, 1)
    assert blamecourt.start_datetime == datetime(1968, 1, 1, 0, 0, 0)
    assert blamecourt.end_date == date(1968, 1, 1)
    assert blamecourt.end_datetime == datetime(1968, 1, 1, 0, 0, 0, 1)
    old_blamecourt_list = towns.filter(depcom='78065')
    assert len(old_blamecourt_list) == 1
    old_blamecourt = old_blamecourt_list[0]
    assert old_blamecourt.id == '78065@1942-01-01'
    assert old_blamecourt.successors == '95065@1968-01-01'
    assert old_blamecourt.modification == CHANGE_COUNTY
    assert old_blamecourt.nccenr == 'Blamécourt'
    assert old_blamecourt.start_date == START_DATE
    assert old_blamecourt.start_datetime == START_DATETIME
    assert old_blamecourt.end_date == date(1967, 12, 31)
    assert (old_blamecourt.end_datetime
            == datetime(1967, 12, 31, 23, 59, 59, 999999))


def test_obsolete():
    """Obsolete town."""
    hauteville_town = town_factory(dep='01', com='459',
                                   nccenr='Hauteville-Lompnés')
    towns = towns_factory(hauteville_town)
    obsolete_record = record_factory(
        dep='01', com='459', mod=OBSOLETE,
        effdate=date(1942, 8, 1), nccoff='Hauteville-Lompnés')
    history = [obsolete_record]
    compute(towns, history)
    hauteville_list = towns.filter(depcom='01459')
    assert len(hauteville_list) == 1
    hauteville = hauteville_list[0]
    assert hauteville.id == '01459@1942-01-01'
    assert hauteville.successors == ''
    assert hauteville.modification == OBSOLETE
    assert hauteville.nccenr == 'Hauteville-Lompnés'
    assert hauteville.start_date == START_DATE
    assert hauteville.start_datetime == START_DATETIME
    assert hauteville.end_date == date(1942, 7, 31)
    assert hauteville.end_datetime == datetime(1942, 7, 31, 23, 59, 59, 999999)


def test_successors_update_on_fusion():
    """When an successor is first set to the wrong town."""
    bragelogne_beauvoir_town = town_factory(dep='10', com='058',
                                            nccenr='Beauvoir')
    beauvoir_sarce_town = town_factory(dep='10', com='036',
                                       nccenr='Beauvoir-sur-Sarce')
    towns = towns_factory(bragelogne_beauvoir_town, beauvoir_sarce_town)
    fusion_association_record = record_factory(
        dep='10', com='036', mod=FUSION_ASSOCIATION_ASSOCIATED,
        effdate=date(1973, 5, 1), nccoff='Beauvoir-sur-Sarce', comech='10058')
    change_name_record = record_factory(
        dep='10', com='058', mod=CHANGE_NAME_FUSION,
        effdate=date(1973, 5, 1), nccoff='Bragelogne-Beauvoir',
        nccanc='Bragelogne')
    history = [fusion_association_record, change_name_record]
    compute(towns, history)
    bragelogne, bragelogne_beauvoir = towns.filter(depcom='10058')
    beauvoir_sur_sarce = towns.filter(depcom='10036')[0]
    assert bragelogne.nccenr == 'Bragelogne'
    assert bragelogne.successors == bragelogne_beauvoir.id
    assert beauvoir_sur_sarce.successors == bragelogne_beauvoir.id
    assert bragelogne_beauvoir.successors == ''


def test_ancestor_not_deleted_on_fusion():
    """The ancestor with same depcom should not be deleted on fusion."""
    val_ocre_town = town_factory(dep='89', com='334', nccenr="Val d'Ocre")
    saint_martin_town = town_factory(dep='89', com='356',
                                     nccenr='Saint-Martin-sur-Ocre')
    towns = towns_factory(val_ocre_town, saint_martin_town)
    creation_delegated_record1 = record_factory(
        dep='89', com='334', mod=CREATION_DELEGATED,
        effdate=date(2016, 1, 1), nccoff='Saint-Aubin-Château-Neuf',
        comech='89334')
    change_name_record1 = record_factory(
        dep='89', com='334', mod=CREATION_DELEGATED_POLE,
        effdate=date(2016, 1, 1), nccoff="Val d'Ocre",
        last=False, comech='89334')
    change_name_record2 = record_factory(
        dep='89', com='334', mod=CREATION_DELEGATED_POLE,
        effdate=date(2016, 1, 1), nccoff="Val d'Ocre",
        last=True, comech='89356')
    creation_delegated_record2 = record_factory(
        dep='89', com='356', mod=CREATION_DELEGATED,
        effdate=date(2016, 1, 1), nccoff='Saint-Martin-sur-Ocre',
        comech='89334')
    history = [creation_delegated_record1, change_name_record1,
               change_name_record2, creation_delegated_record2]
    compute(towns, history)
    saint_aubin, val_ocre = towns.filter(depcom='89334')
    saint_martin_list = towns.filter(depcom='89356')
    assert len(saint_martin_list) == 1
    saint_martin = saint_martin_list[0]
    assert saint_aubin.id == '89334@1942-01-01'
    assert saint_aubin.nccenr == 'Saint-Aubin-Château-Neuf'
    assert saint_aubin.successors == val_ocre.id
    assert saint_martin.id == '89356@1942-01-01'
    assert saint_martin.nccenr == 'Saint-Martin-sur-Ocre'
    assert saint_martin.successors == val_ocre.id
    assert val_ocre.id == '89334@2016-01-01'
    assert val_ocre.nccenr == "Val d'Ocre"
    assert val_ocre.successors == ''


def test_reinstatement_with_existing_town():
    """When a town is reinstated but already exists."""
    avanchers_valmorel_town = town_factory(dep='73', com='024',
                                           nccenr='Avanchers-Valmorel')
    aigueblanche_town = town_factory(dep='73', com='003',
                                     nccenr='Aigueblanche')
    towns = towns_factory(avanchers_valmorel_town, aigueblanche_town)
    fusion_association_record = record_factory(
        dep='73', com='024', mod=FUSION_ASSOCIATION_ASSOCIATED,
        effdate=date(1972, 7, 18), nccoff='Avanchers', comech='73003')
    change_name_record = record_factory(
        dep='73', com='024', mod=CHANGE_NAME,
        effdate=date(1988, 1, 1), nccoff='Avanchers-Valmorel',
        nccanc='Avanchers')
    reinstatement_record = record_factory(
        dep='73', com='024', mod=REINSTATEMENT,
        effdate=date(1988, 1, 1), nccoff='Avanchers-Valmorel',
        comech='73003')
    history = [fusion_association_record, change_name_record,
               reinstatement_record]
    compute(towns, history)
    avanchers, avanchers_valmorel = towns.filter(depcom='73024')
    aigueblanche_list = towns.filter(depcom='73003')
    assert len(aigueblanche_list) == 1
    aigueblanche = aigueblanche_list[0]
    assert avanchers.nccenr == 'Avanchers'
    assert (avanchers.successors
            == aigueblanche.id + ';' + avanchers_valmorel.id)
    assert avanchers_valmorel.nccenr == 'Avanchers-Valmorel'
    assert avanchers_valmorel.successors == ''


def test_start_end_same_moment():
    lamarche_town = town_factory(dep='55', com='273',
                                 nccenr='Lamarche-en-Woëvre')
    heudicourt_town = town_factory(dep='55', com='245',
                                   nccenr='Heudicourt-sous-les-Côtes')
    nonsart_town = town_factory(dep='55', com='386',
                                nccenr='Nonsard-Lamarche')
    towns = towns_factory(lamarche_town, heudicourt_town, nonsart_town)
    fusion_association_record1 = record_factory(
        dep='55', com='273', mod=FUSION_ASSOCIATION_ASSOCIATED,
        effdate=date(1973, 1, 1), nccoff='Lamarche-en-Woëvre', comech='55245')
    reinstatement_record = record_factory(
        dep='55', com='273', mod=REINSTATEMENT,
        effdate=date(1983, 1, 1), nccoff='Lamarche-en-Woëvre', comech='55245')
    fusion_association_record2 = record_factory(
        dep='55', com='273', mod=FUSION_ASSOCIATION_ASSOCIATED,
        effdate=date(1983, 1, 1), nccoff='Lamarche-en-Woëvre', comech='55386')
    history = [fusion_association_record1, reinstatement_record,
               fusion_association_record2]
    compute(towns, history)
    lamarche1, lamarche2 = towns.filter(depcom='55273')
    heudicourt = towns.filter(depcom='55245')[0]
    nonsard = towns.filter(depcom='55386')[0]
    assert lamarche1.nccenr == 'Lamarche-en-Woëvre'
    assert lamarche1.successors == heudicourt.id + ';' + lamarche2.id
    assert lamarche2.nccenr == 'Lamarche-en-Woëvre'
    assert lamarche2.successors == nonsard.id
    assert lamarche2.start_datetime == datetime(1983, 1, 1, 0, 0, 0)
    assert lamarche2.end_datetime == datetime(1983, 1, 1, 0, 0, 0, 1)


def test_creation_delegated_pole_not_sorted():
    """Special case of Boischampré with rangcom not sorted."""
    boischampre_town = town_factory(dep='61', com='375', nccenr='Boischampré')
    vrigny_town = town_factory(dep='61', com='511', nccenr='Vrigny')
    loyer_town = town_factory(dep='61', com='417',
                              nccenr='Saint-Loyer-des-Champs')
    marcei_town = town_factory(dep='61', com='249', nccenr='Marcei')
    towns = towns_factory(
        boischampre_town, vrigny_town, loyer_town, marcei_town)
    creation_delegated_record1 = record_factory(
        dep='61', com='511', mod=CREATION_DELEGATED,
        effdate=date(2015, 1, 1), nccoff='Vrigny', comech='61375')
    creation_delegated_record2 = record_factory(
        dep='61', com='417', mod=CREATION_DELEGATED,
        effdate=date(2015, 1, 1), nccoff='Saint-Loyer-des-Champs',
        comech='61375')
    creation_delegated_record3 = record_factory(
        dep='61', com='249', mod=CREATION_DELEGATED,
        effdate=date(2015, 1, 1), nccoff='Marcei', comech='61375')
    # Here the order is very important given that `rangcom` is not sorted
    # in the right order within the historiq file!
    creation_delegated_pole_record1 = record_factory(
        dep='61', com='375', mod=CREATION_DELEGATED_POLE,
        effdate=date(2015, 1, 1), nccoff='Boischampré', comech='61511',
        last=False)
    creation_delegated_pole_record2 = record_factory(
        dep='61', com='375', mod=CREATION_DELEGATED_POLE,
        effdate=date(2015, 1, 1), nccoff='Boischampré', comech='61417',
        last=False)
    creation_delegated_pole_record3 = record_factory(
        dep='61', com='375', mod=CREATION_DELEGATED_POLE,
        effdate=date(2015, 1, 1), nccoff='Boischampré', comech='61249',
        last=False)
    creation_delegated_pole_record4 = record_factory(
        dep='61', com='375', mod=CREATION_DELEGATED_POLE,
        effdate=date(2015, 1, 1), nccoff='Boischampré', comech='61375',
        last=True)
    history = [
        creation_delegated_record1, creation_delegated_record2,
        creation_delegated_record3,
        creation_delegated_pole_record1, creation_delegated_pole_record2,
        creation_delegated_pole_record3, creation_delegated_pole_record4
    ]
    compute(towns, history)
    boischampre_list = towns.filter(depcom='61375')
    assert len(boischampre_list) == 1
    boischampre = boischampre_list[0]
    vrigny_list = towns.filter(depcom='61511')
    assert len(vrigny_list) == 1
    vrigny = vrigny_list[0]
    assert boischampre.id == '61375@2015-01-01'
    assert boischampre.successors == ''
    assert boischampre.modification == CREATION_DELEGATED_POLE
    assert boischampre.nccenr == 'Boischampré'
    assert vrigny.id == '61511@1942-01-01'
    assert vrigny.successors == boischampre.id
    assert vrigny.modification == CREATION_DELEGATED
    assert vrigny.nccenr == 'Vrigny'


def test_creation_delegated_pole_without_same_name():
    """Special case of Rouget-Pers with name changed."""
    saint_mamet_town = town_factory(dep='15', com='196',
                                    nccenr='Saint-Mamet-la-Salvetat')
    rouget_pers_town = town_factory(dep='15', com='268', nccenr='Rouget-Pers')
    pers_town = town_factory(dep='15', com='150', nccenr='Pers')
    towns = towns_factory(saint_mamet_town, rouget_pers_town, pers_town)
    creation_record = record_factory(
        dep='15', com='268', mod=CREATION,
        effdate=date(1945, 9, 17), nccoff='Rouget', comech='15196')
    # Order is important to make the test pertinent.
    creation_delegated_pole_record1 = record_factory(
        dep='15', com='268', mod=CREATION_DELEGATED_POLE,
        effdate=date(2016, 1, 1), nccoff='Rouget-Pers', comech='15268',
        last=False)
    creation_delegated_record1 = record_factory(
        dep='15', com='150', mod=CREATION_DELEGATED,
        effdate=date(2016, 1, 1), nccoff='Pers', comech='15268')
    creation_delegated_record2 = record_factory(
        dep='15', com='268', mod=CREATION_DELEGATED,
        effdate=date(2016, 1, 1), nccoff='Rouget', comech='15268')
    creation_delegated_pole_record2 = record_factory(
        dep='15', com='268', mod=CREATION_DELEGATED_POLE,
        effdate=date(2016, 1, 1), nccoff='Rouget-Pers', comech='15150',
        last=True)
    history = [
        creation_record,
        creation_delegated_pole_record1,
        creation_delegated_record1,
        creation_delegated_record2,
        creation_delegated_pole_record2,
    ]
    compute(towns, history)
    rouget, rouget_pers = towns.filter(depcom='15268')
    pers_list = towns.filter(depcom='15150')
    assert len(pers_list) == 1
    pers = pers_list[0]
    assert rouget.id == '15268@1945-09-17'
    assert rouget.successors == rouget_pers.id
    assert rouget.modification == CREATION_DELEGATED
    assert rouget.nccenr == 'Rouget'
    assert rouget.start_datetime == datetime(1945, 9, 17, 0, 0, 0)
    assert rouget.end_datetime == datetime(2015, 12, 31, 23, 59, 59, 999999)
    assert pers.id == '15150@1942-01-01'
    assert pers.successors == rouget_pers.id
    assert pers.modification == CREATION_DELEGATED
    assert pers.nccenr == 'Pers'
    assert pers.start_datetime == START_DATETIME
    assert pers.end_datetime == datetime(2015, 12, 31, 23, 59, 59, 999999)
    assert rouget_pers.id == '15268@2016-01-01'
    assert rouget_pers.successors == ''
    assert rouget_pers.modification == CREATION_DELEGATED_POLE
    assert rouget_pers.nccenr == 'Rouget-Pers'
    assert rouget_pers.start_datetime == datetime(2016, 1, 1, 0, 0, 0)
    assert rouget_pers.end_datetime == END_DATETIME


def test_change_county_after_rename():
    """Special case of Sainte-Lucie-de-Tallano"""
    sainte_lucie_town1 = town_factory(dep='2A', com='308',
                                      nccenr='Sainte-Lucie-de-Tallano')
    sainte_lucie_town2 = town_factory(dep='20', com='308',
                                      nccenr='Sainte-Lucie-de-Tallano')
    poggio_town = town_factory(dep='2A', com='237',
                                   nccenr='Poggio-di-Tallano')
    andrea_town = town_factory(dep='2A', com='294',
                               nccenr="Sant'Andréa-di-Tallano")
    towns = towns_factory(
        sainte_lucie_town1, sainte_lucie_town2, poggio_town, andrea_town)
    deletion_fusion_record1 = record_factory(
        dep='2A', com='237', mod=DELETION_FUSION,
        effdate=date(1965, 1, 1), nccoff='Poggio-di-Tallano', comech='2A308')
    deletion_fusion_record2 = record_factory(
        dep='2A', com='294', mod=DELETION_FUSION,
        effdate=date(1965, 1, 1), nccoff="Sant'Andréa-di-Tallano",
        comech='2A308')
    change_name_fusion_record = record_factory(
        dep='2A', com='308', mod=CHANGE_NAME_FUSION, effdate=date(1965, 1, 1),
        nccoff='Sainte-Lucie-de-Tallano', nccanc='Santa-Lucia-di-Tallano')
    change_county_record = record_factory(
        dep='2A', com='308', mod=CHANGE_COUNTY,
        effdate=date(1976, 1, 1), nccoff='Sainte-Lucie-de-Tallano',
        depanc='20308')
    history = [deletion_fusion_record1, deletion_fusion_record2,
               change_name_fusion_record, change_county_record]
    compute(towns, history)
    santa_lucia, sainte_lucie = towns.filter(depcom='20308')
    sainte_lucie_new = towns.filter(depcom='2A308')[0]
    poggio = towns.filter(depcom='2A237')[0]
    andrea = towns.filter(depcom='2A294')[0]
    assert santa_lucia.id == '20308@1942-01-01'
    assert santa_lucia.end_date == date(1964, 12, 31)
    assert sainte_lucie.id == '20308@1965-01-01'
    assert sainte_lucie.end_date == date(1975, 12, 31)
    assert santa_lucia.successors == sainte_lucie.id
    assert poggio.successors == sainte_lucie.id
    assert andrea.successors == sainte_lucie.id
    assert sainte_lucie.successors == sainte_lucie_new.id
    assert sainte_lucie_new.id == '2A308@1976-01-01'
    assert sainte_lucie_new.end_date == END_DATE


'''

Town created after START_DATE and change county later:
Id not found: 2B366@1976-01-01
Successor not found for <Town (20366@1947-04-12): Chisa from 1947-04-12 to 1975-12-31 with successors 2B366@1976-01-01>
Id not found: 95120@1968-01-01
Successor not found for <Town (78692@1948-08-01): Butry-sur-Oise from 1948-08-01 to 1967-12-31 with successors 95120@1968-01-01>

Changed county twice:
Id not found: 78620@1969-11-29
Successor not found for <Town (91620@1942-01-01): Toussus-le-Noble from 1942-01-01 to 1969-11-28 with successors 78620@1969-11-29>
'''
