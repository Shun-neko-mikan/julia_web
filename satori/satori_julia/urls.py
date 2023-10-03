from django.urls import path
from satori_julia import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
]
