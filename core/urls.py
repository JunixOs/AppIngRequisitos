from django.urls import path
from . import views


""" Urls App CORE """
urlpatterns = [
    path("" , views.Inicio , name="index"),
    path("dashboard/" , views.dashboard , name="dashboard"),  
]