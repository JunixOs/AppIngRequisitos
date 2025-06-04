from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from cuentas.models import Moneda, Cuenta
from .models import Usuario
@login_required(login_url='login')
def Index(request):
    Data = {
        "message" : "Mensaje enviado desde Django",
    }
    return render(request , 'index.html')

def Login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        usuario = Usuario.objects.filter(correo=email, contrasena=password).first()

        if usuario:
            print(f"Usuario encontrado: {usuario}")  # Para depuración
            return redirect('core:dashboard')  # o 'index' si tienes así la url
        else:
            error = "Correo o contraseña incorrectos."
    return render(request, 'usuarios/login.html', {'error': error})

def Register(request):
    monedas = Moneda.objects.all()
    cuentas = Cuenta.objects.all()
    if request.method == "POST":
        documento_identidad = request.POST.get('documento_identidad')
        nombres = request.POST.get('nombres')
        apellido_paterno = request.POST.get('apellido_paterno')
        apellido_materno = request.POST.get('apellido_materno')
        correo = request.POST.get('correo')
        saldo = request.POST.get('saldo')
        contrasena = request.POST.get('contrasena')
        telefono = request.POST.get('telefono')
        imagen_perfil = request.FILES.get('imagen_perfil')
        id_moneda = request.POST.get('id_moneda')
        id_cuenta = request.POST.get('id_cuenta')

        imagen_binario = imagen_perfil.read() if imagen_perfil else None

        usuario = Usuario.objects.create(
            documento_identidad=documento_identidad,
            nombres=nombres,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            correo=correo,
            saldo=saldo,
            contrasena=contrasena,
            telefono=telefono,
            imagen_perfil=imagen_binario,
            id_moneda_id=id_moneda,
            id_cuenta_id=id_cuenta
        )
        return redirect('usuarios:login')  # Cambia esto según tu URL de éxito

    return render(request, 'usuarios/register.html', {
        'monedas': monedas,
        'cuentas': cuentas
    })