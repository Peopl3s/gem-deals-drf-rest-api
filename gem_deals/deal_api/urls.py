from django.urls import path

from . import views

app_name = "deal_api"


urlpatterns = [
    path("", views.DealAPIView.as_view(), name="deals"),
]
