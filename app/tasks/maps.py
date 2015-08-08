"""Functions for interacting with maps and geo data."""

import googlemaps  # https://github.com/googlemaps/google-maps-services-python
import json
# import unidecode

import config
from app.models import position as model
from app.tasks import basic_geo
from app.tasks.celery_app import celery_app


class Component(object):

    """Stores an address component."""

    def __init__(self, component):
        """Constructor."""
        self.long_name = component.get('long_name')
        self.short_name = component.get('short_name')
        self.types = component.get('types', [])


class MapLocation(object):

    """Parses a maps result."""

    def __init__(self, result):
        """Initialize object with a map geocode result."""
        self.lat = result['geometry']['location']['lat']
        self.lng = result['geometry']['location']['lng']

        # Observed types:
        # locality, country, political, administrative_area_level_1,
        # administrative_area_level_2, administrative_area_level_3,
        # postal_code, route, bus_station, transit_station, point_of_interest,
        # establishment.
        self.types = result['types']
        self.formatted_address = result['formatted_address']

        self._sublocality = None  # Neighborhood
        self._locality = None  # Town/city
        self._admin_1 = None  # Most often a state or territory
        self._admin_2 = None  # Most often a county or so
        self._country = None  # Most often a county or so

        for component in result['address_components']:
            if 'sublocality_level_1' in component['types']:
                self._sublocality = Component(component)
            elif 'locality' in component['types']:
                self._locality = Component(component)
            elif 'administrative_area_level_1' in component['types']:
                self._admin_1 = Component(component)
            elif 'administrative_area_level_2' in component['types']:
                self._admin_2 = Component(component)
            elif 'country' in component['types']:
                self._country = Component(component)

        # Let's make it easier to debug when things inevitably go wrong.
        self.components = result['address_components']

    @property
    def neighborhood(self):
        """The neighborhood component, if any."""
        return self._sublocality

    @property
    def city(self):
        """The city component."""
        return self._locality

    @property
    def county(self):
        """The county component, if any."""
        return self._admin_2

    @property
    def state(self):
        """The state component."""
        return self._admin_1

    @property
    def country(self):
        """The country component."""
        return self._country

    def IsPlace(self):
        """True if this is a neighborhood or town."""
        return 'locality' in self.types or 'sublocality' in self.types


def _Client():
    return googlemaps.Client(config.GOOGLE_API_KEY)


def SearchByLatLng(lat, lng):
    """Perform a maps search by lat lng."""
    maps = _Client()
    results = maps.reverse_geocode((lat, lng))
    return [MapLocation(result) for result in results]


def SearchByName(name):
    """Perform a maps search by name."""
    maps = _Client()
    results = maps.geocode(name)
    return [MapLocation(result) for result in results]


def SearchByNameNear(name, lat, lng):
    """Search by name and return results sorted by distance to lat/lng."""
    locations = SearchByName(name)
    coord = (lat, lng)
    results = []
    for loc in locations:
        dist = basic_geo.CalculateDistance(coord, (loc.lat, loc.lng)) / 1000
        bearing = basic_geo.CalculateBearing(coord, (loc.lat, loc.lng))
        readable_bearing = basic_geo.ReadableBearing(bearing)
        results.append((dist, readable_bearing, loc))
    results.sort(key=lambda res: res[0], reverse=False)
    return results


# This task's name is registered in app/tasks/spot.py
@celery_app.task
def StoreMapsInformation(row_json):
    """Store location information for a given row."""
    row = json.loads(row_json)
    print 'Retrieving maps info for Position ID %s' % row['id']
    results = SearchByLatLng(row['latitude'], row['longitude'])
    loc = results[0]

    city = loc.city and loc.city.long_name or None
    # city_ascii = unidecode.unidecode(city)  # noqa

    state = loc.state and loc.state.long_name or None
    # state_ascii = unidecode.unidecode(state)  # noqa

    country = loc.country and loc.country.long_name or None
    # country_ascii = unidecode.unidecode(country)  # noqa

    # TODO: Can this be GetPostion.first() instead of list comprehension?
    rows = [r for r in model.GetPositionsByIds([row['id']])]
    if not rows:
        print 'An error has occurred, row %s was not found' % row['id']
        return
    row = rows[0]
    row.city = city
    row.state = state
    row.country = country
    model.UpdatePositions([row])

    # I would like to store state or province or whatever.
    # I did some test searched for "Santa Fe near Guadalajara" and they would
    # show roads and shops and it was a mess. Searching "Santa Fe near Jalisco"
    # gave me the small town nearby. (Searching for "Santa Fe" gave me the
    # New Mexico one and several other US towns.)


def MapsDistance(current, previous):
    """Return the driving distance between two points."""
    _Client()

    # For a matrix of distances:
    # maps.distance_matrix(origins, destinations)

    # For routes:
    # maps.directions(origin, destination)

    # https://developers.google.com/maps/documentation/directions/intro


# This will be registered with app/tasks/spot.py
@celery_app.task
def StoreMapDistance(row_json):
    """Store the map distance for the current row from previous."""
    # This might be modified in the future to support "on_foot"
