from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from usuarios.models import Usuario

import base64
from PIL import Image
import io

""" Views App CUENTAS """
@login_required
def profile(request):
    user_id = request.user.id

    usuario = Usuario.objects.get(id=user_id)
    imagen_bytes = usuario.imagen_perfil
    imagen_base64 = base64.b64encode(imagen_bytes).decode('utf-8')

    formato_imagen = Image.open(io.BytesIO(imagen_bytes)).format

    tab = request.GET.get("tab", "general")
    return render(request, "cuentas/profile.html", {
        "tab": tab , 
        "usuario": usuario,
        "imagen_perfil": imagen_base64,
        "formato_imagen": formato_imagen,
    })

@login_required
def settings(request):
    return render(request, "cuentas/settings.html")