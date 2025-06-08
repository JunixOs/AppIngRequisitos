from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from gestion_financiera_basica.models import Movimiento
from usuarios.models import Usuario

""" Views App CORE """
def Inicio(request):
    if(not request.user.is_authenticated):
        return render(request , 'core/index.html')
    else:
        return redirect('core:dashboard')

@login_required
def dashboard(request):
    user_id = request.user.id

    simbolo_moneda = Usuario.objects.filter(id=user_id).values('id_moneda__simbolo').all()
    simbolo_moneda = simbolo_moneda.first()
    simbolo_moneda = simbolo_moneda["id_moneda__simbolo"]
    movimientos = Movimiento.objects.filter(id_usuario_id=user_id)
    total_balance = Usuario.objects.filter(id=user_id).values('id').annotate(total=Sum('id_cuenta__saldo_cuenta'))
    
    total_balance = total_balance.first()
    total_balance = total_balance['total']

    total_ingresos = Movimiento.objects.filter(id_usuario__id=user_id , tipo="Ingreso").values('id_usuario').annotate(total=Sum('monto')).order_by('id_usuario')
    cantidad_registros_ingresos = Movimiento.objects.filter(id_usuario__id=user_id , tipo="Ingreso").count()


    total_ingresos = total_ingresos.first()
    if(total_ingresos):
        total_ingresos = total_ingresos['total']
    else:
        total_ingresos = "0"

    total_egresos = Movimiento.objects.filter(id_usuario__id=user_id , tipo="Egresos").values('id_usuario').annotate(total=Sum('monto')).order_by('id_usuario')

    total_egresos = total_egresos.first()
    if(total_egresos):
        total_egresos = total_egresos['total']
    else:
        total_egresos = "0"

    if(int(total_egresos) == 0):
        porcentaje_de_ingresos_para_egresos = 0
    else:
        porcentaje_de_ingresos_para_egresos = (float(total_egresos) / float(total_ingresos)) * 100

    tab = request.GET.get("tab", "overview")

    return render(request , 'core/dashboard.html' , {
        "tab": tab,
        "total_balance": total_balance,
        "total_ingresos": total_ingresos,
        "cantidad_ingresos": cantidad_registros_ingresos,

        "total_egresos": total_egresos,
        "porcentaje_de_ingresos_para_egresos": porcentaje_de_ingresos_para_egresos,

        "movimientos": movimientos,
        "simbolo_moneda": simbolo_moneda,
    })

@login_required
def logout_view(request):
    request.session.flush()
    return redirect('core:index')  # Cambia a la URL de login que uses

