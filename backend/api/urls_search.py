from django.urls import path
from .search_api import PropertySearchView

urlpatterns = [
    path('properties', PropertySearchView.as_view(), name='search-properties'),
]
