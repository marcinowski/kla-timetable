from django.db import models


class BusLine(models.Model):
    name = models.TextField(primary_key=True, max_length=5, verbose_name='Bus Line Number')


class BusStop(models.Model):
    name = models.TextField(max_length=200, verbose_name='Bus Stop Name')
    latitude = models.FloatField(verbose_name='Geographical latitude')
    longitude = models.DecimalField(verbose_name='Geographical longitude')
    local_ref = models.DecimalField(null=True, verbose_name='Local Reference ID', max_length=6)
    maps_ref = models.TextField(null=True, max_length=16, verbose_name="OpenMaps Node ID")


class Relation(models.Model):
    start = models.ForeignKey(BusStop, verbose_name="Relation beginning stop", related_name='rel_beg')
    end = models.ForeignKey(BusStop, verbose_name="Relation ending stop", related_name='rel_end')


class Midpoint(models.Model):
    line = models.ForeignKey(BusLine, verbose_name="")
    relation = models.ForeignKey(Relation)
    stop = models.ForeignKey(BusStop)
    hour = models.TextField(max_length=5)
