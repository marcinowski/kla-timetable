import json
import os
import requests
from bs4 import BeautifulSoup

from fetcher import config
from fetcher.kla_results import Result, Line, Relation, BusStop


class KLAConnectionError(Exception):
    """"""


class KLATimeTableFetcher(object):
    backup_file = 'timetable.json'
    """
    Main KLA TimeTable Fetcher scraping HTML from {{config.base_kla_url}}. Uses Result object to represent data.
    """
    # TODO: logging!
    def __init__(self):
        self.current_url = self.get_current_timetable_url()
        self.base_cur_url = self.current_url.rsplit('/', 1)[0]
        self.result = Result()

    def fetch(self):
        """
        Main method for data fetching, returns Result object.
        :return: Result object
        """
        self.get_main_timetable_page()
        self._back_up_results()
        return self.result

    def fetch_from_json_backup(self):
        return Result.from_json()

    def get_main_timetable_page(self):
        """
        Class fetching data from the main timetable view
        (containing all lines and links to the <time_range> timetable
        """
        resp = self._get_response(self.current_url)
        soup = self._adjust(resp)
        rows = soup.find_all('tr')
        for row in rows:
            self.result.lines.append(self._parse_row(row))

    def get_current_timetable_url(self):
        """
        Fetches current timetable url from main page
        :return: current url
        """
        resp = self._get_response(config.timetable_url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        # fixme: during timetable changes there are two timetables available (curr and future)
        element = soup.find(lambda tag: tag.name == config.timetable_tag and config.timetable_text in tag.text)
        url = element.parent.parent.attrs.get('href')
        url = url.strip('.')  # some dots in front of the url
        return config.base_kla_url + url

    @staticmethod
    def _adjust(resp):
        """
        Removes unnecessary parts from main view for easier parsing.
        :param resp: Response object
        :return: BeautifulSoup object
        """
        soup = BeautifulSoup(resp.content, 'html.parser')
        unnecessary_table = soup.find_all('table')[-1]
        unnecessary_table.clear()
        return soup

    def _parse_row(self, row):
        """
        Parses rows in the main timetable view
        :param row: Row containing <line> <relation> (*<time_range_url>*)
        """
        tds = row.find_all('td')
        line_name = tds[0].text.strip()
        route = tds[1].text.strip()
        line = Line(name=line_name)
        for time_range, index in [('daily', 2), ('saturday', 3), ('sunday', 4)]:
            try:
                url = tds[index].find('a').attrs['href']
            except (AttributeError, IndexError):
                continue  # line doesn't operate in given time_range
                # fixme: IndexError is something that needs to be fixed, it's probably SoupParser Error
            line.relations.extend(self._parse_timetable(time_range, url, route))
        return line

    def _parse_timetable(self, time_range, url, route):
        """
        Parses selected time_range timetable for given Line
        :param time_range: daily/saturday/sunday
        :param url: url to selected relations
        :param route: relation name
        :return: list of Relation objects
        """
        base_url, url = url.split('/')
        relations = []
        for i in range(2):
            relation = Relation(name=route, time_range=time_range)
            url = '/'.join((self.base_cur_url, base_url, url))
            resp = self._get_response(url)
            soup = BeautifulSoup(resp.content, 'html.parser')
            relation.bus_stops = self._parse_single_timetable(soup)
            relations.append(relation)
            # stuff below is actually valid only once to switch directions
            url = soup.find('a').attrs['href']
            route = ' - '.join(route.split(' - ')[::-1])
        return relations

    @staticmethod
    def _parse_single_timetable(soup):
        """
        Parses specific timetable view for given time_range, bus_line, relation
        :param soup: BeautifulSoup object
        :return: list of Bus Stops for given relation
        """
        rows = soup.find_all('tr')
        bus_stops = []
        for row in rows[1:]:
            tds = row.find_all('td')
            row_values = list(map(lambda x: x.text.strip(), tds))  # parse columns
            stop = row_values.pop(0)  # first column is BusStop following are hours
            for hour in row_values:
                bus_stops.append(BusStop(name=stop, hour=hour))
        return bus_stops

    @staticmethod
    def _get_response(url):
        """
        Useful method for catching connection errors.
        :param url: url to be requested
        :return: response or raise KLAConnectionError
        """
        try:
            return requests.get(url)
        except requests.RequestException:
            raise KLAConnectionError

    def _back_up_results(self):
        path = os.path.join(config.backups_path, self.backup_file)
        with open(path, 'w') as f:
            json.dump(self.result.to_dict(), f, indent=2)
