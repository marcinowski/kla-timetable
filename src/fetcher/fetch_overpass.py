import os
import overpy

from fetcher import config


class CustomOverpass(overpy.Overpass):
    file = ''

    def parse_json(self, data, encoding="utf-8"):
        self._backup_data(data, encoding, 'json')
        super().parse_json(data, encoding)

    def parse_xml(self, data, encoding="utf-8", parser=None):
        self._backup_data(data, encoding, 'xml')
        super().parse_xml(data, encoding, parser)

    def _backup_data(self, data, encoding, extension):
        file = self.file + '.' + extension
        path = os.path.join(config.backups_path, file)
        open(path, 'w').close()  # clears the file
        if isinstance(data, bytes):
            data = data.decode(encoding)
        with open(path, 'w') as f:
            f.write(data)


class BaseOverpassAPI(CustomOverpass):
    """ Abstract class for Overpass API communication """
    _query = None

    def fetch(self):
        """
        Call this method to get a response from overpass api.
        :return: overpass.Result object
        """
        return self.query(self._query)


class BusStopsCoordinatesFetcher(BaseOverpassAPI):
    """ Class for fetching bus stops coordinates from OpenMaps """
    file = 'bus_stops'
    _query = config.busstops_query


class BusRoutesCoordinatesFetcher(BaseOverpassAPI):
    """ Class for fetching bus routes from OpenMaps """
    file = 'routes'
    _query = config.relation_query
