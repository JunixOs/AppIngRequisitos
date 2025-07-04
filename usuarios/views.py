from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login
from django.core.mail import send_mail
from django.conf import settings


from django.shortcuts import redirect

from cuentas.models import Moneda, Cuenta
from .models import Usuario
import random

def Generar_Pin():
    return str(random.randint(100000, 999999))  # 6 dígitos

def Login(request):
    menssage_change_key = request.GET.get('message_change_key')  # se captura el mensaje
    success_message = request.GET.get('success_message')
    if(menssage_change_key or success_message):
        return render(request, 'usuarios/login.html', {
            'message_change_key': menssage_change_key,
            'success_message': success_message,
        })
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        usuario = authenticate(request , correo=email , password=password)

        if usuario:
            request.session['user_id'] = usuario.id
            
            login(request , usuario , backend='usuarios.backends.EmailBackend')

            email_verificado = request.user.email_verificado

            if(email_verificado):
                return redirect('usuarios:acceso_rapido')
            else:
                return redirect('usuarios:pagina_verificar_correo')
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
        pin_acceso_rapido = "".join(request.POST.get(f"pin_acceso_rapido_{i}") for i in range(1 , 7))
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

        if imagen_perfil:
            import base64
            imagen_b64 = base64.b64encode(imagen_perfil.read()).decode('utf-8')
        else:
            imagen_b64 = None

        registro_temp = {
            'documento_identidad': documento_identidad,
            'nombres': nombres,
            'apellido_paterno': apellido_paterno,
            'apellido_materno': apellido_materno,
            'correo': correo,
            'contrasena': contrasena,
            'telefono': telefono,
            'id_moneda': id_moneda_seleccionada,
            'nombre_cuenta': nombre_cuenta,
            'saldo_inicial': saldo_inicial,
            'descripcion': descripcion,
            'imagen_perfil': imagen_b64,
            'pin_acceso_rapido': pin_acceso_rapido,
            'monedas': monedas,
        }

        if Usuario.objects.filter(correo=correo).exists():
            registro_temp["error"] = "El correo ya está registrado."
            return render(request , "usuarios/register.html" , registro_temp)
        
        if len(pin_acceso_rapido) < 6:
            registro_temp["error"] = "El pin debe tener 6 digitos."
            return render(request , "usuarios/register.html" , registro_temp)

        request.session['registro_temp'] = registro_temp

        return redirect('usuarios:pagina_verificar_correo')

    return render(request, 'usuarios/register.html', {
        'monedas': monedas,
    })

def Pagina_Verificar_Correo(request):
    data = request.session.get('registro_temp')
    user_email = data['correo']

    if(user_email):
        PIN = Generar_Pin()
        request.session['pin_acceso'] = PIN
        request.session['correo_usuario'] = user_email

        send_mail(
            subject='Tu código de acceso rápido - FinGest',
            message=f'Tu código de acceso rapido paraes: {PIN}',        
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )

        return render(request , 'usuarios/validar_correo.html')

def Verificacion_Correo(request):
    if(request.method == 'POST'):
        input_pin = ''.join([
            request.POST.get(f'pin{i}', '') for i in range(6)
        ])

        session_pin = request.session.get('pin_acceso')
        if(input_pin == session_pin):
            data = request.session.get('registro_temp')

            request.session['pin_validado'] = True

            del request.session['pin_acceso']
            del request.session['correo_usuario']

            saldo_inicial = float(data['saldo_inicial'])
            id_moneda_seleccionada = int(data['id_moneda'])

            imagen_binario = None
            if 'imagen_perfil' in data:
                if(data['imagen_perfil']):
                    import base64
                    imagen_binario = base64.b64decode(data['imagen_perfil'])

            moneda = Moneda.objects.get(id=id_moneda_seleccionada)
            usuario = Usuario.objects.create_user(
                documento_identidad=data['documento_identidad'],
                nombres=data['nombres'],
                apellido_paterno=data['apellido_paterno'],
                apellido_materno=data['apellido_materno'],
                correo=data['correo'],
                password=data['contrasena'],
                telefono=data['telefono'],
                imagen_perfil=imagen_binario,
                pin_acceso_rapido=data['pin_acceso_rapido'],
                email_verificado=True,
                id_moneda=moneda
            )

            Cuenta.objects.create(
                id_usuario=usuario,
                nombre=data['nombre_cuenta'],
                saldo_cuenta=saldo_inicial,
                descripcion=data['descripcion'],
            )

            del request.session['registro_temp']

            login(request, usuario, backend='usuarios.backends.EmailBackend')

            return redirect('core:dashboard')
        else:
            return render(request , 'usuarios/validar_correo.html' , { 'error_message' : 'PIN incorrecto'})

@login_required
def Acceso_Rapido(request):
    message = request.GET.get('message_change_key')
    if(message):
        return render(request , 'usuarios/acceso_rapido.html' , {'message_change_key': message})
    
    user = request.user
    if(not user.is_authenticated):
        return redirect('usuarios:login')
    print("Ingreso acceso rapido")

    if(request.method == "POST"):
        pin_input = ''.join([
            request.POST.get(f'pin{i}', '') for i in range(6)
        ])

        if not pin_input.isdigit() or len(pin_input) != 6:
            error_message = "PIN inválido. Ingrese 6 dígitos numéricos."
            return render(request, 'usuarios/acceso_rapido.html', {'error_message': error_message})

        try:
            usuario = Usuario.objects.get(id=user.id)
        except Usuario.DoesNotExist:
            error_message = "Usuario no encontrado."
            return render(request, 'usuarios/acceso_rapido.html', {'error_message': error_message})

        if str(usuario.pin_acceso_rapido).zfill(6) == pin_input:
            request.session['pin_acceso_rapido_validado'] = True

            return redirect('core:dashboard') 
        else:
            error_message = "El PIN ingresado es incorrecto."
            return render(request, 'usuarios/acceso_rapido.html', {'error_message': error_message})

    return render(request , 'usuarios/acceso_rapido.html')

def Reestablecer_Contraseña_O_Pin(request):
    accion = request.GET.get('accion')

    context = {
        'mostrar_pin': False,
        'mostrar_final': False,
        'correo': '',
        'error': '',
        'accion': accion,
    }

    if(request.method == "POST"):
        email = request.POST.get('email')

        # Paso 1: Enviar código
        if 'email' in request.POST and not request.POST.get('pin0'):
            if '@' in email:
                pin = Generar_Pin()
                request.session['pin'] = pin
                request.session['email'] = email
                request.session['accion'] = accion

                send_mail(
                    subject='Tu codigo de verificacion - FinGest',
                    message=f'Tu código de verifiacion es: {pin}',        
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )

                context['mostrar_pin'] = True
                context['correo'] = email
            else:
                context['error'] = "Correo inválido."

        # Paso 2: Verificar PIN
        elif all([request.POST.get(f'pin{i}') for i in range(6)]):
            pin_ingresado = ''.join([request.POST.get(f'pin{i}') for i in range(6)])
            if pin_ingresado == request.session.get('pin'):
                context['mostrar_final'] = True
                context['mostrar_pin'] = False
                context['accion'] = request.session.get('accion')
                context['correo'] = request.session.get('email')
            else:
                context['mostrar_pin'] = True
                context['error'] = "PIN incorrecto, intente nuevamente."
                context['correo'] = request.session.get('email')

        # Paso 3: Formulario final (aquí solo mostramos, no procesamos)
        elif 'nuevo_codigo' in request.POST or 'nuevo_codigo_1' in request.POST:
            user = Usuario.objects.filter(correo=request.session.get('email')).first()
            if(request.session.get('accion') == "cambiar_contraseña"):
                user.set_password(request.POST.get('nuevo_codigo'))
            elif(request.session.get('accion') == "cambiar_pin"):
                pin_nuevo = ''.join(request.POST.get(f'nuevo_codigo_{i}') for i in range(6))
                user.pin_acceso_rapido = pin_nuevo

            user.save()
            accion = request.session.get('accion')
            for key in ['pin', 'email', 'accion']:
                request.session.pop(key, None)

            if(accion == "cambiar_pin"):
                return redirect('/usuarios/acceso_rapido/?message_change_key=Los+cambios+se+realizaron+con+exito')

            return redirect('/usuarios/login/?message_change_key=Los+cambios+se+realizaron+con+exito') # <- se envia el mensaje
    
    return render(request, 'usuarios/verificar_identidad.html', context)
