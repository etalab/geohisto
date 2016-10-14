from collections import namedtuple, OrderedDict

from .constants import DELTA


class Towns(OrderedDict):

    def create(self, town, from_town=None):
        if town.id in self:
            msg = (
                'Attempt to create an existing Town!\n'
                'New: {new_town}\nActual: {actual_town}').format(
                new_town=town, actual_town=self[town.id])
            raise Exception(msg)
        # Update successors references.
        if from_town:
            self.replace_successor(from_town, town)
        self[town.id] = town

    def retrieve(self, id):
        return self[id]

    def update(self, town, to_town=None):
        if town.id not in self:
            msg = 'Attempt to update an unknown Town {town}'.format(town=town)
            raise Exception(msg)
        # Update successors references.
        if to_town and to_town.valid_at(town.end_datetime + DELTA):
            self.replace_successor(town, to_town, town.end_datetime)
        self[town.id] = town

    def delete(self, town):
        # Remove outdated references.
        self.replace_successor(town, '')
        del self[town.id]

    def replace_successor(self, old_successor, new_successor=False,
                          valid_datetime=None):
        if valid_datetime is None:
            is_date_valid = True
        for _, _town in self.items():
            if valid_datetime:
                is_date_valid = (_town.valid_at(valid_datetime)
                                 and not _town.valid_at(valid_datetime + DELTA))
            if old_successor.id in _town.successors and is_date_valid:
                _town = _town.replace_successor(
                    old_successor.id, new_successor and new_successor.id or '')
                self.update(_town)

    def parents(self, id):
        return [town for town in self.values() if id in town.successors]

    def filter(self, depcom):
        _towns = [town for town in self.values() if town.depcom == depcom]
        _towns.sort()  # Useful for tests.
        return _towns

    def with_successors(self):
        return [town for town in self.values() if town.successors]

    def latest(self, depcom):
        """Get the most recent town for a given `depcom`."""
        _towns = self.filter(depcom)
        _towns.sort(key=lambda town: town.end_datetime, reverse=True)
        return _towns[0]

    def valid_at(self, valid_datetime, depcom=None):
        # Beware, ternary operator is tricky here, keep it explicit.
        if depcom:
            _towns = self.filter(depcom)
        else:
            _towns = self.values()
        return [town for town in _towns if town.valid_at(valid_datetime)]

    def get_current(self, depcom, valid_datetime):
        try:
            return self.valid_at(valid_datetime, depcom=depcom)[0]
        except IndexError:
            return self.latest(depcom)


class Town(namedtuple('Town', [
                      'id', 'actual', 'modification', 'successors',
                      'ancestors', 'start_date', 'end_date', 'start_datetime',
                      'end_datetime', 'dep', 'com', 'nccenr', 'depcom',
                      'population'])):
    """Inherit from a namedtuple with empty slots for performances."""
    __slots__ = ()

    # WARNING: do not try to add a property to generate the `depcom`
    # value on the fly, it doubles the time to filter on it later.

    def __repr__(self):
        return ('<Town ({town.id}): {town.nccenr} '
                'from {town.start_date} to {town.end_date}>').format(town=self)

    def generate(self, **kwargs):
        """
        Replace the default private method with a public one.

        Additionnaly, use a more explicit name given it create a new town.
        """
        start_datetime = self.start_datetime
        end_datetime = self.end_datetime
        if 'start_datetime' in kwargs:
            kwargs['start_date'] = kwargs['start_datetime'].date()
            start_datetime = kwargs['start_datetime']
        if 'end_datetime' in kwargs:
            kwargs['end_date'] = kwargs['end_datetime'].date()
            end_datetime = kwargs['end_datetime']
        if start_datetime >= end_datetime:
            msg = (
                'You cannot set {start_datetime} as a start date '
                'and {end_datetime} as an end date for Town {town}.'
            ).format(
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                town=self)
            raise Exception(msg)
        return self._replace(**kwargs)

    def add_modification(self, modification):
        """Append the given modification to the current list if any."""
        if self.modification:
            modification = '{modifications};{modification}'.format(
                modifications=self.modification, modification=modification)
        return self._replace(**{'modification': modification})

    def set_population(self, population):
        return self._replace(**{'population': population})

    def add_ancestor(self, ancestor):
        """Append the given ancestor to the current list if any."""
        if self.ancestors:
            ancestor = self.ancestors + ';' + ancestor
        return self._replace(**{'ancestors': ancestor})

    def add_successor(self, successor):
        """Append the given successor to the current list if any."""
        if self.successors:
            successor = self.successors + ';' + successor
        return self._replace(**{'successors': successor})

    def replace_successor(self, old_successor, new_successor):
        """Replace a successor within the current list."""
        successors = self.successors.replace(old_successor, new_successor)
        return self._replace(**{'successors': successors.strip(';')})

    def clear_successors(self):
        return self._replace(**{'successors': ''})

    def valid_at(self, valid_datetime):
        if valid_datetime is None:
            return False
        return self.start_datetime <= valid_datetime <= self.end_datetime


Record = namedtuple('Record', [
    'depcom', 'mod', 'eff', 'nccoff', 'nccanc', 'comech', 'dep', 'com',
    'depanc', 'nbcom', 'rangcom', 'effdate'
])
