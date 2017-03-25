from collections import namedtuple, OrderedDict

from .constants import DELTA, START_DATETIME


class Towns(OrderedDict):

    def upsert(self, town):
        """Update or insert a Town, return True in case of insertion."""
        is_created = town.id not in self
        self[town.id] = town
        return is_created

    def retrieve(self, id):
        """Get a Town by `id`."""
        try:
            return self[id]
        except KeyError:
            print('Id not found:', id)

    def delete(self, town):
        """Remove a given `town`, do not forget to update references."""
        del self[town.id]

    def update_successors(self, town, from_town=None, to_town=None):
        """Update references in case of a Town rename or creation."""
        try:
            valid_datetime = town.end_datetime + DELTA
        except OverflowError:  # Happens on END_DATETIME + DELTA
            valid_datetime = town.end_datetime
        if to_town and to_town.valid_at(valid_datetime):
            self.replace_successor(town, to_town, town.end_datetime)
        elif from_town and from_town.valid_at(valid_datetime):
            self.replace_successor(from_town, town)

    def replace_successor(self, old_successor, new_successor,
                          valid_datetime=None):
        """Run across all Towns and update successors."""
        if valid_datetime is None:
            is_date_valid = True
        for _town in self.with_successors():
            if valid_datetime:
                try:
                    is_date_valid = _town.valid_at(valid_datetime)
                except OverflowError:  # Happens on END_DATETIME + DELTA
                    is_date_valid = True
            if (old_successor.id in _town.successors and
                    is_date_valid and
                    new_successor.start_datetime != START_DATETIME):
                _town = _town.replace_successor(old_successor.id,
                                                new_successor.id)
                self.upsert(_town)

    def filter(self, **filters):
        """
        Return a (sorted) list of Town with the given filters applied.

        Useful to look up by `depcom`, `nccenr` and so on.
        """
        _towns = [town
                  for town in self.values()
                  for k, v in filters.items()
                  if getattr(town, k) == v]
        _towns.sort()  # Useful for tests.
        return _towns

    def with_successors(self):
        """Return a generator of Towns having successors."""
        return (town for town in self.values() if town.successors)

    def latest(self, depcom):
        """Get the most recent town for a given `depcom`."""
        _towns = self.filter(depcom=depcom)
        _towns.sort(key=lambda town: town.end_datetime, reverse=True)
        return _towns[0]

    def valid_at(self, valid_datetime, depcom=None):
        """Return a list of Towns existing at the given `valid_datetime`."""
        # Beware, ternary operator is tricky here, keep it explicit.
        if depcom:
            _towns = self.filter(depcom=depcom)
        else:
            _towns = self.values()
        return [town for town in _towns if town.valid_at(valid_datetime)]

    def get_current(self, depcom, valid_datetime):
        """Try to return the more pertinent Town given a depcom and date."""
        try:
            return self.valid_at(valid_datetime, depcom=depcom)[0]
        except IndexError:
            return self.latest(depcom)


class Town(namedtuple('Town', [
                      'id', 'actual', 'modification', 'successors',
                      'ancestors', 'start_date', 'end_date', 'start_datetime',
                      'end_datetime', 'dep', 'com', 'nccenr', 'depcom',
                      'population', 'parents'])):
    """Inherit from a namedtuple with empty slots for performances."""
    __slots__ = ()

    # WARNING: do not try to add a property to generate the `depcom`
    # value on the fly, it doubles the time to filter on it later.

    def __repr__(self):
        """Override the default method to be less verbose."""
        return ('<Town ({town.id}): {town.nccenr} '
                'from {town.start_date} to {town.end_date} '
                'with successors {town.successors}>').format(town=self)

    def generate(self, **kwargs):
        """
        Replace the default private method with a public one.

        Additionnaly, use a more explicit name given it generates a new town.
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
        """Update the population."""
        return self._replace(**{'population': population})

    def set_parents(self, parents):
        """Update the parents."""
        return self._replace(**{'parents': parents})

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
        """Remove all successors."""
        return self._replace(**{'successors': ''})

    def valid_at(self, valid_datetime):
        """Check the existence of the Town at a given `valid_datetime`."""
        if valid_datetime is None:
            return False
        return self.start_datetime <= valid_datetime <= self.end_datetime


Record = namedtuple('Record', [
    'depcom', 'mod', 'eff', 'nccoff', 'nccanc', 'comech', 'dep', 'com',
    'depanc', 'last', 'effdate'
])
