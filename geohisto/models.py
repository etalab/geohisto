import logging

from datetime import date
from collections import OrderedDict, namedtuple, defaultdict

from .constants import DELTA, START_DATETIME, END_DATE
from .constants import INTERCOMMUNALITY_INNER_CHANGE
from .constants import INTERCOMMUNALITY_KIND_CHANGE
from .constants import INTERCOMMUNALITY_RENAMED
from .constants import INTERCOMMUNALITY_START_DATE
from .constants import INTERCOMMUNALITY_TAXMODEL_CHANGE

log = logging.getLogger(__name__)


class CollectionMixin:
    """
    Adds some behavior to a `dict` or an `OrderedDict` (any `dict` interface).
    """
    def upsert(self, item):
        """Update or insert an item, return True in case of insertion."""
        is_created = item.id not in self
        self[item.id] = item
        return is_created

    def retrieve(self, id):
        """Get an item by `id`."""
        try:
            return self[id]
        except KeyError:
            log.error('Id not found: %s', id)

    def delete(self, item):
        """Remove a given `item`, do not forget to update references."""
        del self[item.id]

    def replace_successor(self, old_successor, new_successor,
                          valid_datetime=None):
        """Run across all items and update successors."""
        if valid_datetime is None:
            is_date_valid = True
        for _item in self.with_successors():
            if valid_datetime:
                try:
                    is_date_valid = _item.valid_at(valid_datetime)
                except OverflowError:  # Happens on END_DATETIME + DELTA
                    is_date_valid = True
            if (old_successor.id in _item.successors and
                    is_date_valid and
                    new_successor.start_datetime != START_DATETIME):
                _item = _item.replace_successor(old_successor.id,
                                                new_successor.id)
                self.upsert(_item)

    def filter(self, sort=True, **filters):
        """
        Return a (sorted) list of items with the given filters applied.

        Useful to look up by `depcom`, `nccenr` and so on.
        """
        _items = [item
                  for item in self.values()
                  for k, v in filters.items()
                  if getattr(item, k) == v]
        if sort:
            _items.sort()  # Useful for tests. (but very bad for performances)
        return _items

    def with_successors(self):
        """Return a generator of Towns having successors."""
        return (item for item in self.values() if item.successors)


class Towns(CollectionMixin, OrderedDict):
    def latest(self, depcom):
        """Get the most recent town for a given `depcom`."""
        _towns = self.filter(depcom=depcom, sort=False)  # Sort once
        _towns.sort(key=lambda town: town.end_datetime, reverse=True)
        return _towns[0]

    def valid_at(self, valid_datetime, depcom=None):
        """Return a list of Towns existing at the given `valid_datetime`."""
        # Beware, ternary operator is tricky here, keep it explicit.
        if depcom:
            _towns = self.filter(depcom=depcom, sort=False)
        else:
            _towns = self.values()
        return [town for town in _towns if town.valid_at(valid_datetime)]

    def get_current(self, depcom, valid_datetime):
        """Try to return the more pertinent Town given a depcom and date."""
        try:
            return self.valid_at(valid_datetime, depcom=depcom)[0]
        except IndexError:
            return self.latest(depcom)

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


class Item:
    """
    Adds some common behavior to `namedtuple` resulting classes.
    """
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

    def get_ancestors(self, towns):
        """Iterator across ancestors of the current town."""
        for town in towns.with_successors():
            for successor_id in town.successors.split(';'):
                if successor_id == self.id:
                    yield town

    def add_successor(self, successor):
        """Append the given successor to the current list if any."""
        if self.successors:
            successor = self.successors + ';' + successor
        return self._replace(**{'successors': successor})

    def replace_successor(self, old_successor, new_successor):
        """Replace a successor within the current list."""
        successors = self.successors.replace(old_successor, new_successor)
        return self._replace(**{'successors': successors.strip(';')})

    def remove_successor(self, successor):
        """Remove the given successor from the current list."""
        successors = ';'.join([
            succ for succ in self.successors.split(';')
            if succ != successor])
        return self._replace(**{'successors': successors})

    def clear_successors(self):
        """Remove all successors."""
        return self._replace(**{'successors': ''})

    def valid_at(self, valid_datetime):
        """Check the existence of the Town at a given `valid_datetime`."""
        if valid_datetime is None:
            return False
        return self.start_datetime <= valid_datetime <= self.end_datetime


class Town(Item,
           namedtuple('Town', [
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
                'with successors {town.successors} '
                'and mod {town.modification}>').format(town=self)

    @property
    def repr_insee(self):
        """Prepend the INSEE URL (useful for debugging)."""
        insee_base = 'https://www.insee.fr/fr/metadonnees/cog/commune/'
        insee_id = 'COM' + self.depcom + '-' + self.nccenr
        return '{repr} {insee_url}'.format(
            repr=self.__repr__(),
            insee_url='{insee_base}{insee_id}'.format(insee_base=insee_base,
                                                      insee_id=insee_id))

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
        id_ = kwargs.get('id', self.id)
        dep = kwargs.get('dep', self.dep)
        com = kwargs.get('com', self.com)
        depcom = kwargs.get('depcom', self.depcom)
        if depcom != dep + com:
            msg = (
                'You cannot set {dep} as a dep and {com} as a com and '
                '{depcom} as a depcom for Town {town}.'
            ).format(dep=dep, com=com, depcom=depcom, town=self)
            raise Exception(msg)
        if depcom not in id_:
            msg = (
                'You cannot set {id} as an id and {depcom} as a depcom '
                'for Town {town}.'
            ).format(id=id_, depcom=dep + com, town=self)
            raise Exception(msg)
        return self._replace(**kwargs)

    def add_modification(self, modification):
        """Append the given modification to the current list if any."""
        if self.modification:
            modification = '{modifications};{modification}'.format(
                modifications=self.modification, modification=modification)
        return self._replace(**{'modification': modification})


Record = namedtuple('Record', [
    'depcom', 'mod', 'eff', 'nccoff', 'nccanc', 'comech', 'dep', 'com',
    'depanc', 'last', 'effdate'
])


class Intercommunalities(CollectionMixin, defaultdict):
    def latest(self, siren):
        """Get the latest valid intercommunality for a given `siren`."""
        # No need to sort, there is theoricaly only one town
        # with a given siren at a time
        _items = self.filter(siren=siren, end_date=END_DATE, sort=False)
        return _items[0]

    def valid_at(self, valid_date, siren=None):
        """
        Return a list of Intercommunalities existing at the given `valid_date`
        """
        # Beware, ternary operator is tricky here, keep it explicit.
        if siren:
            _items = self.filter(siren=siren)
        else:
            _items = self.values()
        return [item for item in _items if item.valid_at(valid_date)]

    @property
    def open_sirens(self):
        return set(item.siren for item in self.filter(end_date=END_DATE,
                                                      sort=False))

    def ends(self, siren, year, reason):
        intercommunality = self.latest(siren)
        self.upsert(intercommunality.end_on(year, reason))

    def update(self, intercommunality, year):
        current = self.latest(intercommunality.siren)
        changes = []
        if intercommunality.towns != current.towns:
            # This is a perimeter change
            changes.append(INTERCOMMUNALITY_INNER_CHANGE)
        if intercommunality.name != current.name:
            # This is a name change
            changes.append(INTERCOMMUNALITY_RENAMED)
        if intercommunality.kind != current.kind:
            # This is a kind change
            changes.append(INTERCOMMUNALITY_KIND_CHANGE)
        if intercommunality.taxmodel != current.taxmodel:
            # This is a tax model change
            changes.append(INTERCOMMUNALITY_TAXMODEL_CHANGE)

        if changes:
            changes = ';'.join(changes)
            intercommunality = intercommunality.create_on(year, [current.id])
            self.upsert(current.end_on(year, changes, [intercommunality.id]))
            self.upsert(intercommunality)
            return True
        return False


class Intercommunality(Item, namedtuple(
        'Intercommunality', [
            'id',  # GeoID
            'siren',  # SIREN identifier
            'name',  # Normalized name
            'acronym',  # Public acronym, not always initials
            'kind',  # One of CC, CA, CU, CV, DISTRICT, METRO, METRO69, SAN
            'successors',  # List of successors identifiers
            'ancestors',  # List of ancestors identifiers
            'towns',  # Set of components towns identifiers
            'missing_towns',  # Set of towns INSEE code not matched to a town
            'start_date',  # Start validity date
            'end_date',  # End validity date
            'end_reason',  # Reason this intercommunality is ended. See above
            'taxmodel',  # One of 4TX, TPU, FA, FPU
            'population',  # Known population from last census
        ])):
    """
    Represents a French intercommunality or EPCI in French
    """
    # Inherit from a namedtuple with empty slots for performances.
    __slots__ = ()

    def __new__(cls, **kwargs):
        '''Set default values to allow shorter constructors'''
        kwargs.setdefault('id', None)
        kwargs.setdefault('siren', None)
        kwargs.setdefault('name', None)
        kwargs.setdefault('acronym', None)
        kwargs.setdefault('kind', None)
        kwargs.setdefault('start_date', INTERCOMMUNALITY_START_DATE)
        kwargs.setdefault('end_date', END_DATE)
        kwargs.setdefault('end_reason', None)
        kwargs.setdefault('taxmodel', None)
        kwargs.setdefault('population', None)
        # Don't use setdefault on values which are mutable
        kwargs['successors'] = kwargs.get('successors', [])
        kwargs['ancestors'] = kwargs.get('ancestors', [])
        kwargs['towns'] = kwargs.get('towns', set([]))
        kwargs['missing_towns'] = kwargs.get('missing_towns', set([]))
        return super().__new__(cls, **kwargs)

    def create_on(self, year, ancestors=None):
        """
        Instanciate a new intercommunality with start date and id defined.

        Values are populated from the given year
        (intercommunalities are only created or modified on the 1st january)
        Optionnal ancestors can be provided in case of change.
        """
        start_date = date(year, 1, 1)
        id = 'fr:epci:{0}@{1}'.format(self.siren, start_date)
        return self._replace(id=id, start_date=start_date,
                             ancestors=ancestors or [])

    def end_on(self, year, reason, successors=None):
        """
        Instanciate a new intercommunality with end date and reason defined.

        Values are populated from the given year
        (intercommunalities are only created or modified on the 1st january
        so close has to be on the 31st december from the previous year)
        Optionnal successors can be provided in case of change.
        """
        return self._replace(end_date=date(year, 12, 31),
                             end_reason=reason,
                             successors=successors or [])

    @property
    def start_datetime(self):
        '''Property used by `Item.valid_at`'''
        return self.start_date

    @property
    def end_datetime(self):
        '''Property used by `Item.valid_at`'''
        return self.end_date
