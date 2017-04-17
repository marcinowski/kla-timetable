from django.db import models


class Coordinates(models.DecimalField):
    def __init__(self, **kwargs):
        kwargs['max_digits'] = 10
        kwargs['decimal_places'] = 5
        super().__init__(**kwargs)


class CoordinatesBasedModel(models.Model):
    latitude = Coordinates(verbose_name='Geographical latitude')
    longitude = Coordinates(verbose_name='Geographical longitude')


class BusLine(models.Model):
    name = models.TextField(primary_key=True, max_length=5, verbose_name='Bus Line Number')


class BusStop(CoordinatesBasedModel):
    name = models.TextField(max_length=200, verbose_name='Bus Stop Name')
    local_ref = models.TextField(null=True, verbose_name='Local Reference ID', max_length=6)
    maps_ref = models.TextField(null=True, max_length=16, verbose_name="OpenMaps Node ID")


class Relation(models.Model):
    start = models.ForeignKey(BusStop, verbose_name="Relation beginning stop", related_name='rel_beg')
    end = models.ForeignKey(BusStop, verbose_name="Relation ending stop", related_name='rel_end')


class Midpoint(models.Model):
    line = models.ForeignKey(BusLine, verbose_name="")
    relation = models.ForeignKey(Relation)
    stop = models.ForeignKey(BusStop)
    hour = models.TextField(max_length=5, verbose_name='Hour of departure')
    time_range = models.SlugField(verbose_name='Valid days (daily/saturday/sunday)')

"""
Relation proposition:
class Relation:
    previous = FK(Relation)
    bus_stop = FK(BusStop)
    next = FK(Relation)
    line = FK(BusLine)
    hour = TextField
    time_range = TextField/BitField
    expires = DateTimeField
This provides chain-like structure allowing to move back and forth.
"""
