"""Tests related to output validity (duplicity, missing ancestors, etc)."""
from itertools import groupby


def test_unicity_per_boundaries(towns):
    """Ensure unicity for a given insee code at its start/end dates."""
    for depcom, siblings in groupby(towns.values(), lambda town: town.depcom):
        for sibling1 in siblings:
            for sibling2 in siblings:
                if sibling1.id != sibling2.id:
                    assert sibling1.valid_at(sibling2.start_datetime) is False
                    assert sibling1.valid_at(sibling2.end_datetime) is False
