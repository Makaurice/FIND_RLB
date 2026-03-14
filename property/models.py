from django.db import models


class Property(models.Model):
    propertyId = models.AutoField(primary_key=True)
    owner = models.CharField(max_length=100)
    title = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField(blank=True, default='')
    location = models.CharField(max_length=100)
    property_type = models.CharField(max_length=50, blank=True, default='')
    beds = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    sqft = models.IntegerField(default=0)
    year_built = models.IntegerField(null=True, blank=True)
    price = models.IntegerField()
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    amenities = models.JSONField(default=list, blank=True)
    metadataURI = models.CharField(max_length=255, blank=True, default='')
    forRent = models.BooleanField(default=True)
    forSale = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.location} - {self.price}" 
