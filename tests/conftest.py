import pytest

from geohisto.actions import compute
from geohisto.loaders import load_towns, load_history, load_populations
from geohisto.populations import compute_populations
from geohisto.specials import compute_specials
from geohisto.utils import compute_ancestors


@pytest.fixture(scope='module')
def history_list():
    return load_history()


@pytest.fixture(scope='session')
def towns():
    towns = load_towns()
    history_list = load_history()
    populations = load_populations()
    compute(towns, history_list)
    compute_specials(towns)
    compute_ancestors(towns)
    compute_populations(populations, towns)
    return towns
