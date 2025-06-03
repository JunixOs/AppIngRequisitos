from django.urls import path
from . import views

""" Urls App GESTION_FINANCIERA_BASICA """
urlpatterns = [
    path("transactions/", views.transactions, name="transactions"),
    path("savings-goals/", views.savings_goals, name="savings_goals"),
]