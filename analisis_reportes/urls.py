from django.urls import path
from . import views

app_name = "analisis_reportes"
urlpatterns = [
    path('reports/', views.reports, name='reports'),
]