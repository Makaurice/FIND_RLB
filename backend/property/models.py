from django.db import models
from django.conf import settings


class Property(models.Model):
    owner = models.CharField(max_length=100, blank=True, default='')
    title = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField(blank=True, default='')
    location = models.CharField(max_length=255, blank=True, default='')
    property_type = models.CharField(max_length=50, blank=True, default='')
    beds = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    sqft = models.IntegerField(default=0)
    year_built = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(default=0)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    amenities = models.JSONField(default=list, blank=True)
    metadataURI = models.TextField(blank=True, default='')
    forRent = models.BooleanField(default=True)
    forSale = models.BooleanField(default=False)

    class Meta:
        db_table = 'property_property'

    def __str__(self):
        return f"{self.title} ({self.location})"
