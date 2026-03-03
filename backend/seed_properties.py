#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'findrlb_django.settings')
django.setup()

from property.models import Property

# Clear existing data
Property.objects.all().delete()

# Create sample properties
properties = [
    {
        'owner': 'landlord1',
        'title': 'Ocean View 2BR Apartment',
        'location': 'Nyali, Mombasa',
        'property_type': 'Apartment',
        'beds': 2,
        'price': 1250,
        'lat': -4.0435,
        'lon': 39.6636,
        'forRent': True,
    },
    {
        'owner': 'landlord1',
        'title': 'Modern Studio Close to Beach',
        'location': 'Nyali, Mombasa',
        'property_type': 'Studio',
        'beds': 0,
        'price': 850,
        'lat': -4.0430,
        'lon': 39.6650,
        'forRent': True,
    },
    {
        'owner': 'landlord1',
        'title': 'Spacious 3BR Family Home',
        'location': 'Kizingo, Mombasa',
        'property_type': 'House',
        'beds': 3,
        'price': 1900,
        'lat': -4.0500,
        'lon': 39.6590,
        'forRent': True,
    },
    {
        'owner': 'landlord1',
        'title': 'Cozy 1BR Near Beach',
        'location': 'Nyali, Mombasa',
        'property_type': 'Apartment',
        'beds': 1,
        'price': 700,
        'lat': -4.0420,
        'lon': 39.6620,
        'forRent': True,
    },
    {
        'owner': 'landlord1',
        'title': 'Luxe 4BR Penthouse',
        'location': 'Kizingo, Mombasa',
        'property_type': 'Apartment',
        'beds': 4,
        'price': 2500,
        'lat': -4.0502,
        'lon': 39.6595,
        'forRent': True,
    },
    {
        'owner': 'landlord1',
        'title': 'Budget 1BR Studio',
        'location': 'Old Town, Mombasa',
        'property_type': 'Studio',
        'beds': 1,
        'price': 450,
        'lat': -4.0389,
        'lon': 39.6703,
        'forRent': True,
    },
]

for prop in properties:
    Property.objects.create(**prop)

print(f'✓ Created {Property.objects.count()} properties')


