import pickle
import requests
import json
import dateutil.parser

#TODO: Create unit tests for methods of AirlyApi class whether there was no error

class AirlyApi:
    """Class for managing API calls for AirlyApi.

    Address of documentation: https://developer.airly.eu//docs
    """
    def __init__(self, airly_api_key):
        self.base = 'https://airapi.airly.eu'
        self.api_key = airly_api_key

    '''An installation is an entity that binds together a sensor and its location where 
    it's installed at a particular time.'''
    def get_installation(self, installation_id):
        """Endpoint returns single installation metadata, given by installation_id.

        Endpoint: GET /v2/installations/{installationId}

        :param installation_id:  url path parameter; installation identifier
        :return: single installation metadata given by installation_id
        """
        if type(installation_id) != str:
            installation_id = str(installation_id)

        addr_part = '/v2/installations/'
        req = requests.get(self.base+addr_part+installation_id,
                           params={'apikey': self.api_key})
        if req.status_code != 200:
            print("error with request")
            print(req.status_code)
        return req

    def get_installations_nearest(self, latitude, longtitude, max_dist_km, max_results):
        """Endpoint returns list of installations which are closest to a given point,
        sorted by distance to that point.

        Endpoint: GET /v2/installations/nearest

        :param latitude:  latitude as decimal degree, e.g. 50.062006
        :param longtitude: longitude as decimal degree, e.g. 19.940984
        :param max_dist_km: all the returned installations must be located within this limit
         from the given point (in km); negative value means no limit
        :param max_results: maximum number of installations to return; negative value means no limit
        :return: list of installations which are closest to a given point, sorted by distance to that point.
        """

        addr_part = '/v2/installations/nearest'
        req = requests.get(self.base + addr_part,
                           params={'apikey': self.api_key, 'lat': latitude, 'lng': longtitude,
                                   'maxDistanceKM': max_dist_km, 'maxResults': max_results})
        if req.status_code != 200:
            print("error with request")
            print(req.status_code)
        return req

    def get_measurement(self, installation_id):
        """Endpoint returns measurements for concrete installation given by installation_id.

        Endpoint: GET /v2/measurements/installation

        :param installation_id: installation identifier
        :return: measurements for concrete installation given by installation_id
        """

        addr_part = '/v2/measurements/installation'

        req = requests.get(self.base + addr_part,
                           params={'apikey': self.api_key, 'installationId': installation_id})

        if req.status_code != 200:
            print("error with request")
            print(req.status_code)
        return req

    def get_measurement_nearest(self, latitude, longtitude, max_dist_km):
        """Endpoint returns measurements for an installation closest to a given location.

        Endpoint: GET /v2/measurements/nearest

        :param latitude: latitude as decimal degree, e.g. 50.062006
        :param longtitude: longitude as decimal degree, e.g. 19.940984
        :param max_dist_km: the searched installation must be located within this limit
         from the given point (in km); negative value means no limit
        :return: measurements for an installation closest to a given location.
        """

        addr_part = '/v2/measurements/nearest'

        req = requests.get(self.base + addr_part,
                           params={'apikey': self.api_key, 'lat': latitude, 'lng': longtitude,
                                   'maxDistanceKM': max_dist_km})

        if req.status_code != 200:
            print("error with request")
            print(req.status_code)
        return req

    def get_measurement_point(self, latitude, longtitude):
        """Endpoint returns approx. measurements for any geographical location.

        Endpoint: GET /v2/measurements/point

        Measurement values are interpolated by averaging measurements from nearby sensors
        (up to 1,5km away from the given point). The returned value is a weighted average, with the weight
         inversely proportional to the distance from the sensor to the given point.

        :param latitude: latitude as decimal degree, e.g. 50.062006
        :param longtitude: longitude as decimal degree, e.g. 19.940984
        :return: measurement for any geographical location.
        """

        addr_part = '/v2/measurements/nearest'

        req = requests.get(self.base + addr_part,
                           params={'apikey': self.api_key, 'lat': latitude, 'lng': longtitude})

        if req.status_code != 200:
            print("error with request")
            print(req.status_code)
        return req

    def get_meta_indexes(self):
        """Endpoint returns a list of all the index types supported in the API along with lists
        of levels defined per each index type.

        Endpoint: GET /v2/meta/indexes

        :return: a list of all the index types supported in the API along with lists of
        levels defined per each index type.
        """

        addr_part = '/v2/meta/indexes'

        req = requests.get(self.base + addr_part,
                           params={'apikey': self.api_key})

        if req.status_code != 200:
            print("error with request")
            print(req.status_code)
        return req

    def get_meta_measurements(self):
        """Endpoint returns list of all the measurement types supported in the API along with
        their names and units.

        Endpoint: GET /v2/meta/measurements

        :return: list of all the measurement types supported in the API along with
        their names and units
        """

        addr_part = '/v2/meta/measurements'

        req = requests.get(self.base + addr_part,
                           params={'apikey': self.api_key})

        if req.status_code != 200:
            print("error with request")
            print(req.status_code)
        return req


class PickledSites:
    """Class for temporary storing AirlyApi responses because of limited number of possible API calls."""
    def __init__(self, airly_api_key):
        self.airly_api = AirlyApi(airly_api_key)
        self.data_installation_metadata = None
        self.data_installations_metadata = None
        self.data_measurement = None
        self.data_measurement_nearest = None
        self.data_measurement_point = None
        self.data_meta_measurements = None
        self.data_meta_indexes = None

    def save_all(self):
        self.save_installation()
        self.save_installations_nearest()
        self.save_measurement()
        self.save_measurement_nearest()
        self.save_measurement_point()
        self.save_meta_indexes()
        self.save_meta_measurements()

    def save_installation(self, installation_id=7468):
        data = self.airly_api.get_installation(installation_id)
        self._pickle(data, 'data_installation_metadata.pkl')

    def save_installations_nearest(self, latitude=52.410751, longtitude=16.905636,
                                   max_dist_km=8, max_results=10):
        data = self.airly_api.get_installations_nearest(latitude, longtitude, max_dist_km, max_results)
        self._pickle(data, 'data_installations_metadata.pkl')

    def save_measurement(self, installation_id=7468):
        data = self.airly_api.get_measurement(installation_id)
        self._pickle(data, 'data_measurement_by_id.pkl')

    def save_measurement_nearest(self, latitude=52.410751, longtitude=16.905636, max_dist_km=8):
        data = self.airly_api.get_measurement_nearest(latitude, longtitude, max_dist_km)
        self._pickle(data, 'data_measurement_nearest.pkl')

    def save_measurement_point(self, latitude=52.410751, longtitude=16.905636):
        data = self.airly_api.get_measurement_point(latitude, longtitude)
        self._pickle(data, 'data_measurement_point.pkl')

    def save_meta_indexes(self):
        data = self.airly_api.get_meta_indexes()
        self._pickle(data, 'data_meta_indexes.pkl')

    def save_meta_measurements(self):
        data = self.airly_api.get_meta_measurements()
        self._pickle(data, 'data_meta_measurements.pkl')

    def load_all(self):
        data_jsons = [self.get_installation(), self.get_installations_nearest(), self.get_measurement(),
                      self.get_measurement_nearest(), self.get_measurement_point(), self.get_meta_indexes(),
                      self.get_meta_measurements()]
        return data_jsons

    def get_installation(self):
        self.data_installation_metadata = self._unpickle('data_installation_metadata.pkl')
        return self.data_installation_metadata

    def get_installations_nearest(self):
        self.data_installations_metadata = self._unpickle('data_installations_metadata.pkl')
        return self.data_installations_metadata

    def get_measurement(self):
        self.data_measurement = self._unpickle('data_measurement_by_id.pkl')
        return self.data_measurement

    def get_measurement_nearest(self):
        self.data_measurement_nearest = self._unpickle('data_measurement_nearest.pkl')
        return self.data_measurement_nearest

    def get_measurement_point(self):
        self.data_measurement_point = self._unpickle('data_measurement_point.pkl')
        return self.data_measurement_point

    def get_meta_indexes(self):
        self.data_meta_indexes = self._unpickle('data_meta_indexes.pkl')
        return self.data_meta_indexes

    def get_meta_measurements(self):
        self.data_meta_measurements = self._unpickle('data_meta_measurements.pkl')
        return self.data_meta_measurements

    @staticmethod
    def _unpickle(pkl_name, mode='rb'):
        with open(pkl_name, mode) as f:
            data = pickle.load(f)
        return data

    @staticmethod
    def _pickle(data, pkl_name, mode='wb'):
        with open(pkl_name, mode) as f:
            pickle.dump(data, f)


class Weather:
    """Class represents weather at the given place and time.

    Class shows temp, humid, pressure, PM1, PM10, PM25 (+-) in specific location or installation.
    """
    #TODO: work on history data and predicitions

    def __init__(self):
        self.weather_json = None
        self.latitude = None
        self.longtitude = None
        self.datetime = None
        self.measurements = dict.fromkeys(
            ['PM1', 'PM10', 'PM25', 'PRESSURE', 'HUMIDITY', 'TEMPERATURE'], None)

        self.standards = {}
        self.indexes = {}

    def _process_current_data(self, weather_data):

        data_from_datetime = dateutil.parser.parse(
            weather_data['fromDateTime']).strftime("%Y-%m-%d %H:%M:%S")
        data_till_datetime = dateutil.parser.parse(
            weather_data['tillDateTime']).strftime("%Y-%m-%d %H:%M:%S")
        self.datetime = data_till_datetime
        # print(f'Measuring from {data_from_datetime} to {data_till_datetime}.')

        for meas in weather_data['values']:
            if meas['name'] in self.measurements:
                self.measurements[meas['name']] = meas['value']

    def _process_indexes(self, indexes_list):
        for index in indexes_list:
            index_info = {'value': index['value'], 'level': index['level'],
                          'description': index['description'], 'color': index['color']}
            self.indexes[index['name']] = index_info
        #print('INDEXES: ', self.indexes)

    def _process_standards(self, standards_list):
        for standard in standards_list:
            standard_info = {'authority': standard['name'], 'limit': standard['limit']}
            self.standards[standard['pollutant']] = standard_info
        #print('STANDARDS: ', self.standards)

    def process_weather_data(self, weather_json):
        """Process json data about weather and store it in class variables"""
        self.weather_json = json.loads(weather_json)
        current_data = self.weather_json['current']

        self._process_current_data(current_data)
        self._process_indexes(current_data['indexes'])
        self._process_standards(current_data['standards'])



