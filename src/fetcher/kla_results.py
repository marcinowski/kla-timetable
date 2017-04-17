class Result(object):
    """
    Result class for obtaining timetable info.
    Structure is following:
    Result:
        -> lines (list of lines)
            -> name (line number)
            -> relations (list of relations)
                -> relation (start - end bus stops)
                -> time_range (daily, saturday, sunday)
                -> bus_stops (list of bus stops)
                    -> name (bus stop name)
                    -> hour (hour of departure)
    """

    def __init__(self, since='', expires=''):
        self.since = since
        self.expires = expires
        self.lines = []

    def __repr__(self):
        return "<Result object> from: {}, expires: {}".format(self.since, self.expires)

    # todo: serialization to json (overriding JSONEncoder)
    def to_dict(self):
        return {'since': self.since, 'expires': self.expires, 'lines': [l.to_dict() for l in self.lines]}

    def from_json(self):
        pass  # todo: deserialization from json


class Line(object):
    """
    Single Line in the timetable
    """

    def __init__(self, name=''):
        self.name = name
        self.relations = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Line object #{}>".format(self.name)

    def to_dict(self):
        return {'name': self.name, 'relations': [r.to_dict() for r in self.relations]}


class Relation(object):
    """
    Relation 'First stop - Last stop'
    """

    def __init__(self, name='', time_range=''):
        self.name = name
        self.time_range = time_range  # daily, saturday, sunday
        self.bus_stops = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Relation object {} {}>".format(self.name, self.time_range)

    def to_dict(self):
        return {'name': self.name, 'time_range': self.time_range, 'bus_stops': [b.to_dict() for b in self.bus_stops]}


class BusStop(object):
    """
    Name of bus stop with hour of departure for given relation
    """

    def __init__(self, name='', hour=''):
        self.name = name
        self.hour = hour

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<BusStop object {}>".format(self.name)

    def to_dict(self):
        return {'name': self.name, 'hour': self.hour}
