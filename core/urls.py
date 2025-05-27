from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.Home, name='Pagina de Inicio Primario'),
    path('' , views.Inicio , name="Pagina de Inicio Secundario"),
]