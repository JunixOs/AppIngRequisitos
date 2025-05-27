from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login, name='Login Users'),
    path('register/', views.Register, name='Register Users'),
]