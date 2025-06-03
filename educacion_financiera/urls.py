from django.urls import path
from . import views

""" Urls App EDUCACION_FINANCIERA """
urlpatterns = [
    path("calculators/", views.calculators, name="calculators"),
    path("courses/", views.courses, name="courses"),
    path("tips/", views.tips, name="tips"),
]