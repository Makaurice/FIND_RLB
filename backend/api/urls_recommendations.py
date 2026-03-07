from django.urls import path

from .recommendations import RecommendationsView

urlpatterns = [
    path('', RecommendationsView.as_view(), name='recommendations'),
]
