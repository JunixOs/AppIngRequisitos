from django.urls import path
from . import views

""" Urls App CUENTAS """
app_name = "cuentas"
urlpatterns = [
    path("perfil/" , views.Perfil , name="perfil"),
    path("actualizar_imagen_perfil/" , views.Actualizar_Imagen_Perfil , name="actualizar_imagen_perfil"),
    path("modificar_perfil/", views.Modificar_Perfil , name="modificar_perfil"),
    path("modificar_seguridad_perfil/" , views.Cambiar_Contraseña , name="modificar_seguridad_perfil"),
    path("settings/", views.settings, name="settings"),
    
]