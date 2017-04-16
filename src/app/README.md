#Use Cases:
 1. show route for given line on given relation
 2. find connection between two points with one/multiple lines for given time
 3. show timetable for bus stops

#Given Data available:
 - bus stop coordinates
 - timetable for each line and bus stop

#Models Structure:

BusLine:
- name

BusStop:
- name
- coordinates

Relation:
- start -> BusStop
- end -> BusStop

Midpoint:
- line -> BusLine
- relation -> Relation
- stop -> BusStop
- hour

#Use Cases solutions for applied schema:
1. Midpoint.objects.filter(line=<line>, relation=<relation>).stop_set.all()
2. Following steps are taken
 - locate closest stops for beginning and end of the journey
 - get all lines from the closest stops and see if routes intersect
 - if not try to optimize time/walking distance
3. BusStop.objects.get(<bus_stop>).midpoint_set.all()
