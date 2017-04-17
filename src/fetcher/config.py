import os
from django.conf import settings

timetable_url = 'http://www.kla.com.pl/cat,1'
base_kla_url = 'http://www.kla.com.pl'
timetable_tag = 'strong'
timetable_text = 'Tabelaryczny rozkład jazdy'
timetable_columns = ['line', 'route', 'daily', 'saturday', 'sunday', 'additional']
coords_bbox = '51.63208355839104,17.7923583984375,51.81286001413873,18.2373046875'
backups_path = os.path.join(settings.BASE_DIR, 'fetcher', 'backups')
relation_query = """[out:json];(relation({bbox})[route=bus][operator~"Kaliskie Linie Autobusowe|KLA"];);
out body;>;out skel qt;""".format(bbox=coords_bbox)
busstops_query = """[out:json];(node({bbox})[highway=bus_stop];);out body;>;out skel qt;""".format(bbox=coords_bbox)
