from decimal import Decimal
from app.models import BusStop, BusLine


class BaseOverpassParser(object):
    """ Abstract class for common methods """
    @classmethod
    def parse(cls, data):
        raise NotImplemented


class BusStopsParser(BaseOverpassParser):
    """ Parser for Bus Stops models """
    @classmethod
    def parse(cls, data):
        for bs in data.nodes:
            cls._parse_node(bs)

    @staticmethod
    def _parse_node(bs):
        defaults = {
            'latitude': Decimal(bs.lat),
            'longitude': Decimal(bs.lon),
            'local_ref': bs.tags.get('local_ref', '')
        }
        BusStop.objects.update_or_create(
            name=bs.tags.get('name', ''),
            maps_ref=bs.id,
            defaults=defaults
        )


class BusRoutesParser(BaseOverpassParser):
    """ Parser for Bus Stops models """
    @classmethod
    def parse(cls, data):
        for rel in data.relations:
            cls._parse_relation(rel)

    @classmethod
    def _parse_relation(cls, rel):
        """
        Method for relation handling, relation is an object roughly describing START<->END relation
        of a BusLine.
        :param rel: overpy.Relation
        """
        line = rel.tags.get('ref').strip()
        bl, created = BusLine.objects.get_or_create(name=line)
        if created:
            pass  # TODO: add method verifying new busLine
        for member in rel.members:
            way = member.resolve()
            cls._parse_way(way)

    @classmethod
    def _parse_member(cls, member):
        """
        Method for handling members (RelationWay), it describes a set of ways that form a relation.
        :param member: overpy.RelationWay
        """
        way = member.resolve()
        cls._parse_way(way)

    @staticmethod
    def _parse_way(way):
        """
        Method for handling way, way is an object containing multiple nodes describing it's path.
        :param way: overpy.Way
        """
        pass  # TODO: what to do with ways


class BusTimetablesParser(BaseOverpassParser):
    """ Parser for Bus Stops models """
    @classmethod
    def parse(cls, data):
        pass
