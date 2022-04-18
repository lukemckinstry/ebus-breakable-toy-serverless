from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf.global_settings import LANGUAGES
import uuid
import pytz
TIMEZONES = [tuple([i,i]) for i in pytz.all_timezones]

ROUTE_TYPES = [('0', 'Tram, Streetcar, Light rail'),
			   ('1','Subway, Metro'),
			   ('2','Rail'),
			   ('3','Bus'),
			   ('4','Ferry'),
			   ('5','Cable Car'),
			   ('6','Gondola'),
			   ('7','Funicular')]

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
    accepted_domains = ArrayField(models.CharField(max_length=100), blank=True, null=True)

    def __str__(self):
        return self.agency_name +':'+ self.agency_id


class Route(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    #from gtfs

    route_id = models.CharField(max_length=50) #required
    agency_id = models.ForeignKey(Agency, on_delete=models.CASCADE)
    route_short_name = models.CharField(max_length=50, blank=True) #conditionaly required
    route_long_name = models.CharField(max_length=100, blank=True) #conditionaly required
    route_desc = models.CharField(max_length=500, )
    route_type = models.CharField(max_length=50, choices=ROUTE_TYPES) #required, this will always be 3
    route_url = models.CharField(max_length=100, blank=True)
    route_color = models.CharField(max_length=50, blank=True)
    route_text_color = models.CharField(max_length=50, blank=True)
    route_sort_order = models.CharField(max_length=50, blank=True)


    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiLineStringField(srid=4326,blank=True,null=True)

    route_distance = models.FloatField(blank=True,null=True) ### calculated 

    trips_monday = models.IntegerField(blank=True)
    trips_tuesday = models.IntegerField(blank=True)
    trips_wednesday = models.IntegerField(blank=True)
    trips_thursday = models.IntegerField(blank=True)
    trips_friday = models.IntegerField(blank=True)
    trips_saturday = models.IntegerField(blank=True)
    trips_sunday = models.IntegerField(blank=True)

    ### user managed fields 
    zev_charging_infrastrucutre = models.BooleanField(default=False)
    zev_notes = models.TextField(blank=True,null=True)
    pct_zev_service = models.FloatField(blank=True,null=True)
    num_zev = models.IntegerField(blank=True,null=True) 


    # Returns the string representation of the model.
    def __str__(self):
        return self.route_long_name + ' (' + self.route_id + ')'