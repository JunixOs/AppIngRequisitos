from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout

from django.shortcuts import redirect

from cuentas.models import Moneda, Cuenta
from .models import Usuario

def Login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        usuario = authenticate(request , correo=email , password=password)

        if usuario:
            request.session['user_id'] = usuario.id
            
            login(request , usuario , backend='usuarios.backends.EmailBackend')

            return redirect('core:dashboard')  # o 'index' si tienes así la url
        else:
            return render(request, 'usuarios/login.html' , {
                "message_error": "Credenciales no validas.",
            })

    return render(request, 'usuarios/login.html')


def Register(request):
    monedas = Moneda.objects.all()

    if request.method == "POST":
        documento_identidad = request.POST.get('documento_identidad')
        nombres = request.POST.get('nombres')
        apellido_paterno = request.POST.get('apellido_paterno')
        apellido_materno = request.POST.get('apellido_materno')
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        telefono = request.POST.get('telefono')
        imagen_perfil = request.FILES.get('imagen_perfil')

        id_moneda_seleccionada = request.POST.get('id_moneda')
        try:
            moneda_obj = Moneda.objects.get(id=id_moneda_seleccionada)
        except Moneda.DoesNotExist:
            error = "La moneda seleccionada no es válida."
            return render(request, "usuarios/register.html", {"error": error, 'monedas': monedas})

        nombre_cuenta = request.POST.get('nombre_cuenta')
        saldo_inicial = request.POST.get('saldo_inicial')
        descripcion = request.POST.get('descripcion_cuenta')

        if not descripcion:
            descripcion = ""
        if not nombre_cuenta:
            nombre_cuenta = "Cuenta principal"

        try:
            saldo_inicial_float = float(saldo_inicial)
        except (ValueError, TypeError):
            error = "El saldo inicial debe ser un número válido."
            return render(request, "usuarios/register.html", {"error": error, 'monedas': monedas})

        imagen_binario = imagen_perfil.read() if imagen_perfil else None

        if Usuario.objects.filter(correo=correo).exists():
            error = "El correo ya está registrado."
            return render(request, "usuarios/register.html", {"error": error, 'monedas': monedas})

        cuenta = Cuenta.objects.create(
            nombre=nombre_cuenta,
            descripcion=descripcion,
            saldo_cuenta=saldo_inicial_float,
        )

        usuario = Usuario.objects.create_user(
            documento_identidad=documento_identidad,
            nombres=nombres,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            correo=correo,
            password=contrasena,
            telefono=telefono,
            imagen_perfil=imagen_binario,
            id_moneda=moneda_obj,
            id_cuenta=cuenta,
        )

        login(request, usuario, backend='usuarios.backends.EmailBackend')

        return redirect('core:dashboard')

    return render(request, 'usuarios/register.html', {
        'monedas': monedas,
    })

@login_required
def Fast_Access():
    pass