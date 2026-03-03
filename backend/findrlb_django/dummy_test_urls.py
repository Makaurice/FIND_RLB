from django.urls import path

def _noop_view(request):
    raise RuntimeError("dummy view should not be called in unit tests")

urlpatterns = [
    path('', _noop_view),
]
