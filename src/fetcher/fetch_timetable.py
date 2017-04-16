import re
import requests
from bs4 import BeautifulSoup

from fetcher import config


class KLAConnectionError(Exception):
    """"""

BASE_URL = 'http://www.kla.com.pl'


class KLATimeTableFetcher(object):
    def __init__(self):
        self.current_url = self.get_current_timetable_url()
        self.structure = []
        self.base_cur_url = self.current_url.rsplit('/', 1)[0]

    def fetch(self):
        self.get_main_timetable_page()

    def get_main_timetable_page(self):
        resp = self._get_response(self.current_url)
        soup = self._adjust(resp)
        rows = soup.find_all('tr')
        for row in rows:
            self._parse_row(row)

    def get_current_timetable_url(self):
        resp = self._get_response(config.timetable_url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        element = soup.find(lambda tag: tag.name == config.timetable_tag and config.timetable_text in tag.text)
        url = element.parent.parent.attrs.get('href')
        url = url.strip('.')  # some dots in front of the url
        return BASE_URL + url

    def _adjust(self, resp):
        soup = BeautifulSoup(resp.content, 'html.parser')
        unnecessary_table = soup.find_all('table')[-1]
        unnecessary_table.clear()
        return soup

    def _parse_row(self, row):
        tds = row.find_all('td')
        line = tds[0].text.strip()
        route = tds[1].text.strip()
        u = {name: tds[index].find('a').attrs['href'] for name, index in [('daily', 2), ('saturday', 3), ('sunday', 4)]}
        self._parse_row_data(line, route, u)

    def _parse_row_data(self, line, route, urls):
        results = [self._parse_timetable(name, url) for name, url in urls.items()]
        routes = [route, ' - '.join(route.split(' - ')[::-1])]
        data = {routes[i]: list(filter(lambda x: x[i], results)) for i in range(2)}  # fixme: structure??
        self.structure.append({'line': line, 'routes': data})

    def _parse_timetable(self, name, url):
        structure = []
        base_url, url = url.split('/')
        for i in range(2):
            url = '/'.join((self.base_cur_url, base_url, url))
            resp = self._get_response(url)
            soup = BeautifulSoup(resp.content, 'html.parser')
            results = self._parse_single_timetable(soup)
            url = soup.find('a').attrs['href']  # this is actually valid only once to switch directions
            structure.append({name: results})
        return structure

    def _parse_single_timetable(self, soup):
        rows = soup.find_all('tr')
        structure = []
        for row in rows[1:]:
            tds = row.find_all('td')
            hours = list(map(lambda x: x.text.strip(), tds))
            stop = hours.pop(0)
            structure.append({'stop': stop, 'hours': hours})
        return structure

    @staticmethod
    def _get_response(url):
        try:
            return requests.get(url)
        except requests.RequestException:
            raise KLAConnectionError
