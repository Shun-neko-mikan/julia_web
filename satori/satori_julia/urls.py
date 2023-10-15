from django.urls import path
from satori_julia import views

urlpatterns = [
    path("julia", views.IndexView.as_view(), name="index"),
    path("cal_julia", views.cal_julia, name="cal_julia"),
]
