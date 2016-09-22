from collections import namedtuple, OrderedDict

from .constants import END_DATE


class Towns:

    def __init__(self):
        self._towns = OrderedDict()

    def __len__(self):
        return len(self._towns)

    def __iadd__(self, town):
        self._towns[town.id] = town
        return self

    def __iter__(self):
        for id, town in self._towns.items():
            yield id, town

    def get(self, id):
        try:
            return self._towns[id]
        except KeyError:
            print('TODO: {id} not found in towns.'.format(id=id))

    def parents(self, id):
        return [town for town in self._towns.values() if id in town.successors]

    def filter(self, depcom):
        towns = [town for town in self._towns.values()
                 if town.depcom == depcom]
        towns.sort()  # Useful for tests.
        return towns

    def with_successors(self):
        return [town for town in self._towns.values() if town.successors]

    def latest(self, depcom):
        """Get the most recent town for a given `depcom`."""
        towns = [town for town in self._towns.values()
                 if town.depcom == depcom]
        towns.sort(key=lambda t: t.end_datetime, reverse=True)
        return towns[0]

    def remove(self, town):
        del self._towns[town.id]

    def valid_at(self, valid_datetime):
        return [town for town in self._towns.values()
                if town.start_datetime <= valid_datetime < town.end_datetime]


Town = namedtuple('Town', [
    'id', 'actual', 'modification', 'successors', 'ancestors',
    'start_date', 'end_date', 'start_datetime', 'end_datetime',
    'depcom', 'dep', 'com', 'nccenr', 'population'
])


class HistoryList:

    def __init__(self):
        self._histories = []

    def __len__(self):
        return len(self._histories)

    def __iadd__(self, history):
        self._histories.append(history)
        return self

    def filter(self, depcom):
        return [history for history in self._histories
                if history.depcom == depcom]

    def filter_by_mod(self, mod):
        return [history for history in self._histories if history.mod == mod]

    def filter_by_mods(self, mods):
        return [history for history in self._histories if history.mod in mods]


History = namedtuple('History', [
    'depcom', 'mod', 'eff', 'nccoff', 'nccanc', 'comech', 'dep', 'com',
    'depanc', 'effdate'
])
