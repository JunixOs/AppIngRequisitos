# gestion_financiera_basica/forms.py
from django import forms
from .models import Movimiento


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['nombre', 'tipo', 'monto', 'fecha_movimiento', 'descripcion', 'id_cuenta', 'id_usuario']
        widgets = {
            'fecha_movimiento': forms.DateInput(attrs={'type': 'text'}, ),
            
        }