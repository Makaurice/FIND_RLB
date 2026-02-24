from django.shortcuts import render
from django.http import JsonResponse
from .models import Property
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def property_list(request):
	if request.method == 'GET':
		properties = list(Property.objects.all().values())
		return JsonResponse(properties, safe=False)
	elif request.method == 'POST':
		data = json.loads(request.body)
		prop = Property.objects.create(
			owner=data.get('owner', ''),
			location=data.get('location', ''),
			metadataURI=data.get('metadataURI', ''),
			forRent=data.get('forRent', True),
			forSale=data.get('forSale', False),
			price=data.get('price', 0)
		)
		return JsonResponse({'propertyId': prop.propertyId}, status=201)
