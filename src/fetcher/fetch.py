from fetcher.fetch_overpass import BusRoutesCoordinatesFetcher, BusStopsCoordinatesFetcher
from fetcher.fetch_timetable import KLATimeTableFetcher

from .parsers import BusRoutesParser, BusStopsParser, BusTimetablesParser
from app.models import BusStop, BusLine


class DataFetcher(object):
    """ Class for integrating data sources and database """
    def __init__(self):
        pass

    @classmethod
    def fetch(cls):
        """
        Downloads, parses and saves bus stops, bus routes and bus timetables in this order.
        :return:
        """
        cls.fetch_bus_stops()
        cls.fetch_bus_routes()
        cls.fetch_bus_timetables()

    @classmethod
    def fetch_bus_stops(cls):
        bus_stops = BusStopsCoordinatesFetcher().fetch()
        BusStopsParser.parse(bus_stops)

    @classmethod
    def fetch_bus_routes(cls):
        bus_routes = BusRoutesCoordinatesFetcher().fetch()
        BusRoutesParser.parse(bus_routes)

    @classmethod
    def fetch_bus_timetables(cls):
        bus_timetables = KLATimeTableFetcher().fetch()
        BusTimetablesParser.parse(bus_timetables)
