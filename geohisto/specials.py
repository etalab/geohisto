"""Special cases handled manually."""
import inspect
from datetime import date, datetime

from geohisto import specials
from .constants import START_DATE, START_DATETIME
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
        end_datetime=datetime(2012, 12, 31, 23, 59, 59, 999999),
        successors=bauge_en_anjou_new.id
    )
    towns.upsert(bauge_en_anjou_new)
    towns.upsert(bauge_old)
    towns.update_successors(
        bauge_en_anjou_new, from_town=bauge_en_anjou_current)
    towns.delete(bauge_en_anjou_current)


def compute_specials(towns):
    """Apply all special case functions from that file."""
    for name, func in inspect.getmembers(specials, inspect.isfunction):
        if name.startswith('_special_case_'):
            func(towns)
