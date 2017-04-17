import os
import overpy

from fetcher import config


class DataBackupDoesNotExist(Exception):
    """"""


class CustomOverpass(overpy.Overpass):
    file = ''

    def parse_json(self, data, encoding="utf-8"):
        self._backup_data(data, encoding, self.json_path)
        return super().parse_json(data, encoding)

    def parse_xml(self, data, encoding="utf-8", parser=None):
        self._backup_data(data, encoding, self.xml_path)
        return super().parse_xml(data, encoding, parser)

    def _backup_data(self, data, encoding, path):
        if isinstance(data, bytes):
            data = data.decode(encoding)
        with open(path, 'w') as f:
            f.write(data)

    @property
    def json_path(self):
        file = self.file + '.json'
        return os.path.join(config.backups_path, file)

    @property
    def xml_path(self):
        file = self.file + '.xml'
        return os.path.join(config.backups_path, file)


class BaseOverpassAPI(CustomOverpass):
    """ Abstract class for Overpass API communication """
    _query = None

    def fetch(self):
        """
        Call this method to get a response from overpass api.
        :return: overpass.Result object
        """
        return self.query(self._query)

    def fetch_from_json_backup(self):
        """
        Call this method to get a result object from saved json data.
        :return: overpass.Result object
        """
        backup = self._fetch_from_backup(self.json_path)
        return overpy.Result.from_json(data=backup)

    def fetch_from_xml_backup(self):
        """
        Call this method to get a result object from saved xml data.
        :return: overpass.Result object
        """
        backup = self._fetch_from_backup(self.xml_path)
        return overpy.Result.from_xml(data=backup)

    @staticmethod
    def _fetch_from_backup(path):
        if not os.path.exists(path):
            raise DataBackupDoesNotExist("The path {} contains no backup data".format(path))
        with open(path, 'r') as f:
            backup = f.read()
        return backup


class BusStopsCoordinatesFetcher(BaseOverpassAPI):
    """ Class for fetching bus stops coordinates from OpenMaps """
    file = 'bus_stops'
    _query = config.busstops_query


class BusRoutesCoordinatesFetcher(BaseOverpassAPI):
    """ Class for fetching bus routes from OpenMaps """
    file = 'routes'
    _query = config.relation_query
