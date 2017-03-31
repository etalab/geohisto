"""Special cases handled manually."""
import inspect
from datetime import date, datetime

from geohisto import specials
from .constants import DELTA, END_DATETIME, START_DATE, START_DATETIME
from .utils import compute_id, only_if_depcom


@only_if_depcom('49018')
def _special_case_bauge_en_anjou(towns):
    """Special case: items order where last is not the last in historiq.

    Which results in a prematured deletion of Baugé-en-Anjou…
    """
    bauge_current, bauge_en_anjou_current = towns.filter(depcom='49018')
    bauge_en_anjou_new = bauge_en_anjou_current.generate(
        id=compute_id(bauge_en_anjou_current.depcom, date(2013, 1, 1)),
        start_datetime=datetime(2013, 1, 1)
    )
    bauge_old = bauge_current.generate(
        id=compute_id(bauge_current.depcom, START_DATE),
        start_datetime=START_DATETIME,
        end_datetime=bauge_en_anjou_new.start_datetime - DELTA,
        successors=bauge_en_anjou_new.id
    )
    towns.upsert(bauge_en_anjou_new)
    towns.upsert(bauge_old)
    towns.update_successors(
        bauge_en_anjou_new, from_town=bauge_en_anjou_current)
    towns.delete(bauge_en_anjou_current)


@only_if_depcom('28131')
def _special_case_dommerville(towns):
    """Special case: county changed and successor not updated."""
    dommerville_current = towns.filter(depcom='28131')[0]
    dommerville_new = dommerville_current.replace_successor(
        'COM91016@1942-01-01', 'COM91016@1968-01-01')
    towns.upsert(dommerville_new)


@only_if_depcom('69274')
def _special_case_crepieux_pape(towns):
    """Special case: county changed and successor not updated."""
    crepieux_current = towns.filter(depcom='69274')[0]
    crepieux_new = crepieux_current.replace_successor(
        'COM69286@1942-01-01', 'COM69286@1972-12-15')
    towns.upsert(crepieux_new)


@only_if_depcom('95065')
def _special_case_blamecourt(towns):
    """Special case: county changed and successor not updated.

    Giving it a 1ms lifespan given that it does not exist anymore.

    It is a bit ambiguous on INSEE website:
    * https://www.insee.fr/fr/metadonnees/cog/commune/COM95065-Blamecourt
    * https://www.insee.fr/fr/metadonnees/cog/commune/COM78065-Blamecourt
    """
    blamecourt_current = towns.filter(depcom='95065')[0]
    blamecourt_new = blamecourt_current.generate(
        end_datetime=blamecourt_current.start_datetime + DELTA
    )
    blamecourt_new = blamecourt_new.replace_successor(
        'COM95355@1942-01-01', 'COM95355@1968-01-01')
    towns.upsert(blamecourt_new)


@only_if_depcom('95025')
def _special_case_arthieul(towns):
    """Special case: county changed and successor not updated.

    Giving it a 1ms lifespan given that it does not exist anymore.

    It is a bit ambiguous on INSEE website:
    * https://www.insee.fr/fr/metadonnees/cog/commune/COM95025-Arthieul
    * https://www.insee.fr/fr/metadonnees/cog/commune/COM78025-Arthieul
    """
    arthieul_current = towns.filter(depcom='95025')[0]
    arthieul_new = arthieul_current.generate(
        end_datetime=arthieul_current.start_datetime + DELTA
    )
    arthieul_new = arthieul_new.replace_successor(
        'COM95355@1942-01-01', 'COM95355@1968-01-01')
    towns.upsert(arthieul_new)


@only_if_depcom('20366')
def _special_case_chisa(towns):
    """Special case: county changed and id not updated."""
    chisa_wrong, chisa_old = towns.filter(depcom='20366')
    chisa_new = chisa_wrong.generate(id='COM2B366@1976-01-01')
    towns.upsert(chisa_new)
    towns.delete(chisa_wrong)


@only_if_depcom('78692')
def _special_case_butry_oise(towns):
    """Special case: county changed and id not updated."""
    butry_oise_wrong, butry_oise_old = towns.filter(depcom='78692')
    butry_oise_new = butry_oise_wrong.generate(id='COM95120@1968-01-01')
    towns.upsert(butry_oise_new)
    towns.delete(butry_oise_wrong)


@only_if_depcom('91620')
def _special_case_toussus_noble(towns):
    """Special case: inexisting entry.

    Even bugged on INSEE website:
    * https://www.insee.fr/fr/metadonnees/cog/commune/COM91620-Toussus-le-Noble
    * https://www.insee.fr/fr/metadonnees/cog/commune/COM78620-Toussus-le-Noble
    """
    toussus_noble_old = towns.filter(depcom='91620')[0]
    toussus_noble_new = toussus_noble_old.generate(
        id='COM78620@1969-11-29',
        start_datetime=toussus_noble_old.end_datetime + DELTA,
        end_datetime=END_DATETIME,
        successors=''
    )
    towns.upsert(toussus_noble_new)


def compute_specials(towns):
    """Apply all special case functions from that file."""
    for name, func in inspect.getmembers(specials, inspect.isfunction):
        if name.startswith('_special_case_'):
            func(towns)
