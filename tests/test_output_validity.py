"""Tests related to output validity (duplicity, missing ancestors, etc)."""


def test_unicity_per_boundaries(towns):
    """Ensure unicity for a given insee code at its start/end dates."""
    for town_id, town in towns.items():
        for sibling in towns.filter(depcom=town.depcom):
            if sibling.id != town.id:
                assert sibling.valid_at(town.start_datetime) is False
                assert sibling.valid_at(town.end_datetime) is False
