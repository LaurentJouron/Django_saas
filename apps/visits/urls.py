from django.urls import path

from .views import VisitsView

app_name = "visits"

urlpatterns = [
    path("", VisitsView.as_view(), name="visits"),
]
