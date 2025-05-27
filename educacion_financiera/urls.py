from django.urls import path
from . import views

urlpatterns = [
    path('ayuda/', views.Ayuda, name='Ayuda'),
    path('contacto/' , views.Contacto , name='Contacto')
]