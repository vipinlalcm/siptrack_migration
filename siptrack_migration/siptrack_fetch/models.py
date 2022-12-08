# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Associations(models.Model):
    self_oid = models.CharField(primary_key=True, max_length=16)
    other_oid = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'associations'
        app_label = 'siptrack_fetch'
        unique_together = (('self_oid', 'other_oid'),)


class DeviceConfigData(models.Model):
    oid = models.CharField(primary_key=True, max_length=16)
    data = models.TextField(blank=True, null=True)
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'device_config_data'
        app_label = 'siptrack_fetch'
        unique_together = (('oid', 'timestamp'),)


class Idmap(models.Model):
    parent_oid = models.CharField(max_length=16, blank=True, null=True)
    oid = models.CharField(primary_key=True, max_length=16)
    class_id = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'idmap'


class Nodedata(models.Model):
    oid = models.CharField(primary_key=True, max_length=16)
    name = models.CharField(max_length=64)
    datatype = models.CharField(max_length=16, blank=True, null=True)
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nodedata'
        app_label = 'siptrack_fetch'
        unique_together = (('oid', 'name'),)


class Version(models.Model):
    version = models.CharField(primary_key=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'version'
