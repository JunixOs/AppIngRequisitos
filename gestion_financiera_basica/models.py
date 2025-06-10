from django.db import models

# Create your models here.

class MetaAhorro(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_limite = models.DateTimeField()
    monto_objetivo = models.DecimalField(max_digits=15, decimal_places=2)
    frecuencia_aporte = models.DateTimeField()
    descripcion = models.CharField(max_length=255)
    nombre = models.CharField(max_length=50)
    id_usuario = models.ForeignKey("usuarios.Usuario", on_delete=models.CASCADE)
    id_cuenta = models.ForeignKey("cuentas.Cuenta", on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class MoldeAhorro(models.Model):
    nombre = models.CharField(max_length=50)
    porcentaje_ahorro = models.DecimalField(max_digits=3, decimal_places=2)
    id_meta_ahorro = models.ForeignKey(MetaAhorro, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Movimiento(models.Model):
    TIPOS_MOVIMIENTO = (
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    )

    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=25, choices=TIPOS_MOVIMIENTO)
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    fecha_movimiento = models.DateTimeField()
    descripcion = models.CharField(max_length=300)
    id_cuenta = models.ForeignKey("cuentas.Cuenta", on_delete=models.CASCADE)
    id_usuario = models.ForeignKey("usuarios.Usuario", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo} - {self.monto}"

