"""Tests related to special cases handled manually."""
from datetime import date, datetime

from geohisto.actions import compute
from geohisto.constants import (
    START_DATETIME, END_DATETIME,
    CREATION_DELEGATED, CREATION_DELEGATED_POLE,
    CREATION_PREEXISTING_DELEGATED
)
from geohisto.specials import compute_specials
from .factories import towns_factory, town_factory, record_factory


def test_creation_preexisting_delegated():
    """Special case of Baugé with a last item that is not the last!"""
    towns = towns_factory(
        town_factory(dep='49', com='018', nccenr='Baugé-en-Anjou'),
        town_factory(dep='49', com='213', nccenr='Montpollin'),
        town_factory(dep='49', com='245', nccenr='Pontigné'),
        town_factory(dep='49', com='303', nccenr="Saint-Martin-d'Arcé"),
        town_factory(dep='49', com='372', nccenr='Vieil-Baugé'),
        town_factory(dep='49', com='315',
                     nccenr='Saint-Quentin-lès-Beaurepaire')
    )

    # Order is important to make the test relevant.
    history = [
        record_factory(
            dep='49', com='213', effdate=date(2016, 1, 1),
            mod=CREATION_PREEXISTING_DELEGATED, comech='49018',
            nccoff='Montpollin'),
        record_factory(
            dep='49', com='018', effdate=date(2013, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49213',
            nccoff='Baugé-en-Anjou'),
        record_factory(
            dep='49', com='018', effdate=date(2013, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49245',
            nccoff='Baugé-en-Anjou'),
        record_factory(
            dep='49', com='018', effdate=date(2013, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49303',
            nccoff='Baugé-en-Anjou'),
        record_factory(
            dep='49', com='018', effdate=date(2013, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49372',
            nccoff='Baugé-en-Anjou', last=True),
        record_factory(
            dep='49', com='213', effdate=date(2013, 1, 1),
            mod=CREATION_DELEGATED, comech='49018',
            nccoff='Montpollin'),
        record_factory(
            dep='49', com='245', effdate=date(2013, 1, 1),
            mod=CREATION_DELEGATED, comech='49018',
            nccoff='Pontigné'),
        record_factory(
            dep='49', com='303', effdate=date(2013, 1, 1),
            mod=CREATION_DELEGATED, comech='49018',
            nccoff="Saint-Martin-d'Arcé"),
        record_factory(
            dep='49', com='372', effdate=date(2013, 1, 1),
            mod=CREATION_DELEGATED, comech='49018',
            nccoff='Vieil-Baugé'),
        record_factory(
            dep='49', com='018', effdate=date(2013, 1, 1),
            mod=CREATION_DELEGATED, comech='49018',
            nccoff='Baugé'),
        record_factory(
            dep='49', com='018', effdate=date(2013, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49018',
            nccoff='Baugé-en-Anjou'),
        record_factory(
            dep='49', com='245', effdate=date(2016, 1, 1),
            mod=CREATION_PREEXISTING_DELEGATED, comech='49018',
            nccoff='Pontigné'),
        record_factory(
            dep='49', com='303', effdate=date(2016, 1, 1),
            mod=CREATION_PREEXISTING_DELEGATED, comech='49018',
            nccoff="Saint-Martin-d'Arcé"),
        record_factory(
            dep='49', com='315', effdate=date(2016, 1, 1),
            mod=CREATION_DELEGATED, comech='49018',
            nccoff='Saint-Quentin-lès-Beaurepaire'),
        record_factory(
            dep='49', com='372', effdate=date(2016, 1, 1),
            mod=CREATION_PREEXISTING_DELEGATED, comech='49018',
            nccoff='Vieil-Baugé'),
        record_factory(
            dep='49', com='018', effdate=date(2016, 1, 1),
            mod=CREATION_PREEXISTING_DELEGATED, comech='49018',
            nccoff='Baugé'),
        record_factory(
            dep='49', com='018', effdate=date(2016, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49018',
            nccoff='Baugé-en-Anjou'),
        record_factory(
            dep='49', com='018', effdate=date(2016, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49031',
            nccoff='Baugé-en-Anjou'),
        record_factory(
            dep='49', com='018', effdate=date(2016, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49079',
            nccoff='Baugé-en-Anjou'),
        record_factory(
            dep='49', com='018', effdate=date(2016, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49097',
            nccoff='Baugé-en-Anjou'),
        record_factory(
            dep='49', com='018', effdate=date(2016, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49101',
            nccoff='Baugé-en-Anjou'),
        record_factory(
            dep='49', com='018', effdate=date(2016, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49116',
            nccoff='Baugé-en-Anjou'),
        record_factory(
            dep='49', com='018', effdate=date(2016, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49128',
            nccoff='Baugé-en-Anjou'),
        record_factory(
            dep='49', com='018', effdate=date(2016, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49143',
            nccoff='Baugé-en-Anjou'),
        record_factory(
            dep='49', com='018', effdate=date(2016, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49157',
            nccoff='Baugé-en-Anjou'),
        record_factory(
            dep='49', com='018', effdate=date(2016, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49213',
            nccoff='Baugé-en-Anjou'),
        record_factory(
            dep='49', com='018', effdate=date(2016, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49245',
            nccoff='Baugé-en-Anjou'),
        record_factory(
            dep='49', com='018', effdate=date(2016, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49303',
            nccoff='Baugé-en-Anjou'),
        record_factory(
            dep='49', com='018', effdate=date(2016, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49315',
            nccoff='Baugé-en-Anjou'),
        record_factory(
            dep='49', com='018', effdate=date(2016, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49372',
            nccoff='Baugé-en-Anjou'),
        record_factory(
            dep='49', com='018', effdate=date(2016, 1, 1),
            mod=CREATION_DELEGATED_POLE, comech='49380',
            nccoff='Baugé-en-Anjou', last=True)
    ]
    compute(towns, history)
    compute_specials(towns)
    bauge, bauge_en_anjou = towns.filter(depcom='49018')
    montpollin = towns.filter(depcom='49213')[0]
    saint_quentin = towns.filter(depcom='49315')[0]
    assert bauge.id == 'COM49018@1942-01-01'
    assert bauge.start_datetime == START_DATETIME
    assert bauge.end_datetime == datetime(2012, 12, 31, 23, 59, 59, 999999)
    assert bauge.successors == bauge_en_anjou.id
    assert montpollin.id == 'COM49213@1942-01-01'
    assert montpollin.start_datetime == START_DATETIME
    assert (montpollin.end_datetime ==
            datetime(2012, 12, 31, 23, 59, 59, 999999))
    assert montpollin.successors == bauge_en_anjou.id
    assert saint_quentin.id == 'COM49315@1942-01-01'
    assert saint_quentin.start_datetime == START_DATETIME
    assert (saint_quentin.end_datetime ==
            datetime(2015, 12, 31, 23, 59, 59, 999999))
    assert saint_quentin.successors == bauge_en_anjou.id
    assert bauge_en_anjou.id == 'COM49018@2013-01-01'
    assert bauge_en_anjou.start_datetime == datetime(2013, 1, 1, 0, 0, 0)
    assert bauge_en_anjou.end_datetime == END_DATETIME
    assert bauge_en_anjou.successors == ''


'''
COM08270@1942-01-01,08270,1942-01-01 00:00:00,1966-08-06 23:59:59,Malmy,
COM08115@2016-01-01,,DEP08@1860-07-01,NULL,310
COM08270@1942-01-01,08270,1942-01-01 00:00:00,1966-08-06 23:59:59,Malmy,
COM08115@1959-04-26,,DEP08@1860-07-01,NULL,310

3               44  08  270         1   08115   0       MALMY       Malmy
1   0   0       44  08  115 3   19  1       0       CHEMERY-CHEHERY
Chémery-Chéhéry     Vouziers

08  3   19  115 D24-04-1959 25-04-1959  26-04-1959  26-04-1959  100
                             0   Chémery-sur-Bar 0   Chémery
08          270 D27-07-1966 06-08-1966  07-08-1966  07-08-1966  310
08115                       0   Malmy
08  3   19  115 A17-10-1964 08-12-1964  01-11-1964  01-11-1964  320         1
 1   08129                       0   Chémery-sur-Bar
08  3   19  115 D27-07-1966 06-08-1966  07-08-1966  07-08-1966  320         1
 1   08270                       0   Chémery-sur-Bar

08      19  115 A29-12-2015 30-01-2016  01-01-2016  01-01-2016  331
     08115                       0   Chémery-sur-Bar
08      19  115 A29-12-2015 30-01-2016  01-01-2016  01-01-2016  331
     08115                       0   Chémery-sur-Bar
08  3   19  115 A29-12-2015 30-01-2016  01-01-2016  01-01-2016  341         2
 1   08114                       0   Chémery-Chéhéry
08  3   19  115 A29-12-2015 30-01-2016  01-01-2016  01-01-2016  341         2
 2   08115                       0   Chémery-Chéhéry

'''


'''
Town created after START_DATE and change county later:
Id not found: COM2B366@1976-01-01
Successor not found for <Town (COM20366@1947-04-12):
Chisa from 1947-04-12 to 1975-12-31
with successors COM2B366@1976-01-01>
Id not found: COM95120@1968-01-01
Successor not found for <Town (COM78692@1948-08-01):
Butry-sur-Oise from 1948-08-01 to 1967-12-31
with successors COM95120@1968-01-01>

Changed county twice:
Id not found: COM78620@1969-11-29
Successor not found for <Town (COM91620@1942-01-01):
Toussus-le-Noble from 1942-01-01 to 1969-11-28
with successors COM78620@1969-11-29>
'''
