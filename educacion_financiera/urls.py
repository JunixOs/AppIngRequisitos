from django.urls import path
from . import views

""" Urls App EDUCACION_FINANCIERA """
app_name = "educacion_financiera"
urlpatterns = [
    path("calculators/", views.calculators, name="calculators"),
    path("courses/", views.courses, name="courses"),
    path("tips/", views.tips, name="tips"),
]