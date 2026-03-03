from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class PropertySearchView(APIView):
    """Public property search endpoint that accepts query params for filters, sorting, and radius search.
    Supported query params:
      - price_min, price_max (integers)
      - beds (integer)
      - property_type (string)
      - location (string substring match)
      - lat, lon (floats) and radius_km (float) for geographic radius search
      - sort_by (price|beds) and order (asc|desc)
    """

    def haversine_km(self, lat1, lon1, lat2, lon2):
        from math import radians, sin, cos, sqrt, asin
        R = 6371.0
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        return R * c

    def get(self, request):
        # helper functions to parse query params safely
        def parse_int(key):
            v = request.query_params.get(key)
            if v is None or v == '':
                return None
            try:
                return int(v)
            except ValueError:
                return None

        def parse_float(key):
            v = request.query_params.get(key)
            if v is None or v == '':
                return None
            try:
                return float(v)
            except ValueError:
                return None

        # parse incoming filters/sorting/radius params
        price_min = parse_int('price_min')
        price_max = parse_int('price_max')
        beds = parse_int('beds')
        property_type = request.query_params.get('property_type')
        location = request.query_params.get('location')
        lat = parse_float('lat')
        lon = parse_float('lon')
        radius_km = parse_float('radius_km')
        sort_by = request.query_params.get('sort_by')
        order = request.query_params.get('order', 'asc')

        # build queryset and apply filters via ORM
        from property.models import Property
        qs = Property.objects.all()
        if price_min is not None:
            qs = qs.filter(price__gte=price_min)
        if price_max is not None:
            qs = qs.filter(price__lte=price_max)
        if beds is not None:
            qs = qs.filter(beds__gte=beds)
        if property_type:
            qs = qs.filter(property_type__iexact=property_type)
        if location:
            qs = qs.filter(location__icontains=location)

        # convert queryset results to list of dictionaries for later processing
        results = list(qs.values('id', 'title', 'location', 'property_type', 'beds', 'price', 'lat', 'lon'))

        # radius filtering (use calculated distance attribute)
        if lat is not None and lon is not None and radius_km is not None:
            filtered = []
            for p in results:
                plat = p.get('lat')
                plon = p.get('lon')
                if plat is None or plon is None:
                    continue
                d = self.haversine_km(lat, lon, plat, plon)
                if d <= radius_km:
                    p = p.copy()
                    p['distance_km'] = round(d, 3)
                    filtered.append(p)
            results = filtered

        # sorting
        if sort_by in ('price', 'beds', 'distance_km'):
            reverse = (order == 'desc')
            results = sorted(results, key=lambda x: x.get(sort_by, 0), reverse=reverse)

        return Response(results)
