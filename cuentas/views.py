from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render , redirect
from django.http import HttpResponse
from usuarios.models import Usuario
from core.decorators import fast_access_pin_verified

import base64
from PIL import Image
import io

""" Views App CUENTAS """
@login_required
@fast_access_pin_verified
def Perfil(request):
    usuario = Usuario.objects.filter(id=request.user.id).first()
    formato_imagen = None
    imagen_base64 = None
    hay_imagen_perfil = False
    if(usuario.imagen_perfil):
        imagen_bytes = usuario.imagen_perfil
        imagen_base64 = base64.b64encode(imagen_bytes).decode('utf-8')

        formato_imagen = Image.open(io.BytesIO(imagen_bytes)).format
        hay_imagen_perfil = True

    tab = request.GET.get("tab", "general")

    success_message = request.GET.get("success_message")

    return render(request, "cuentas/profile.html", {
        "tab": tab , 
        "usuario": usuario,
        "imagen_perfil": imagen_base64,
        "formato_imagen": formato_imagen,
        "hay_imagen_perfil": hay_imagen_perfil,
        "success_message": success_message,
    })

@login_required
@fast_access_pin_verified
def Modificar_Perfil(request):
    user_id = request.user.id

    if(request.method == "POST"):
        nombres = request.POST.get("nombres")
        apellido_paterno = request.POST.get("apellido_paterno")
        apellido_materno = request.POST.get("apellido_materno")
        email = request.POST.get("email")
        if(Usuario.objects.filter(correo=email).exists()):
            return render(request , "cuentas/perfil/" , {"tab": "general" , "error_message": "El correo ingresado ya esta en uso."})
        
        telefono = request.POST.get("telefono")

        Usuario.objects.filter(id=user_id).update(
            nombres = nombres,
            apellido_paterno = apellido_paterno,
            apellido_materno = apellido_materno,
            correo = email,
            telefono = telefono,
        )

        return redirect("/cuentas/perfil/?tab=general&success_message=Informacion+modificada+con+exito")

@login_required
@fast_access_pin_verified
def Actualizar_Imagen_Perfil(request):
    if(request.method == "POST"):
        imagen_perfil = request.FILES.get('foto_perfil')
        if(imagen_perfil):
            Usuario.objects.filter(id=request.user.id).update(
                imagen_perfil=imagen_perfil.read(),
            )
            return redirect("/cuentas/perfil/?tab=general&success_message=Imagen+subida+con+exito")


@login_required
@fast_access_pin_verified
def Cambiar_Contraseña(request):
    if(request.method == "POST"):
        contaseña_actual_ingresada = request.POST.get("actual_password")
        if(request.user.check_password(contaseña_actual_ingresada)):
            nueva_contraseña = request.POST.get("new_password")
            request.user.set_password(nueva_contraseña)
            request.user.save()

            return redirect('/cuentas/perfil/?tab=security&success_message=Contraseña+cambiada+con+exito')
        else:
            error_message = "La contraseña actual es incorrecta."
            return render(request , 'cuentas/profile.html' , {"tab": "security" , "error_message": error_message,})

@login_required
@fast_access_pin_verified
def settings(request):
    return render(request, "cuentas/settings.html")