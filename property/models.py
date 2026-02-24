from django.db import models

class Property(models.Model):
	propertyId = models.AutoField(primary_key=True)
	owner = models.CharField(max_length=100)
	location = models.CharField(max_length=100)
	metadataURI = models.CharField(max_length=255)
	forRent = models.BooleanField(default=True)
	forSale = models.BooleanField(default=False)
	price = models.IntegerField()

	def __str__(self):
		return f"{self.location} - {self.price}" 
