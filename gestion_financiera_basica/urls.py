from django.urls import path
from . import views

""" Urls App GESTION_FINANCIERA_BASICA """
app_name = "gestion_financiera_basica"
urlpatterns = [
    path("transactions/", views.transactions, name="transactions"),
    path("savings-goals/", views.savings_goals, name="savings_goals"),
    path('movimientos/agregar/', views.agregar_movimiento, name='agregar_movimiento'),
]