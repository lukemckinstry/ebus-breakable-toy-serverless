from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf.global_settings import LANGUAGES
import uuid
import pytz
TIMEZONES = [tuple([i,i]) for i in pytz.all_timezones]


class Agency(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, blank=False)
    
    ### from gtfs

    agency_id = models.CharField(max_length=100, blank=True)
    agency_name = models.CharField(max_length=100) #required
    agency_url = models.CharField(max_length=100) #required
    agency_timezone = models.CharField(max_length=50,blank=True, null=True, choices=TIMEZONES) #required
    agency_lang = models.CharField(max_length=50, blank=True, null=True, choices=LANGUAGES)
    agency_phone = models.CharField(max_length=20, blank=True)
    agency_fare_url = models.CharField(max_length=100, blank=True)
    agency_email = models.EmailField(max_length=100, blank=True)

    ### managed in app
    num_vehicles = models.IntegerField(blank=True, null=True)
    num_zero_emission_vehicles = models.IntegerField(blank=True, null=True)
    gtfs_url = models.CharField(max_length=100, blank=True) ## for management process
    accepted_domains = ArrayField(models.CharField(max_length=100), blank=True)

    def __str__(self):
        return self.agency_name +':'+ self.agency_id