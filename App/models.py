from django.db import models
from django.contrib.auth.models import AbstractUser


class Moneda(models.Model):
    codigo = models.CharField(max_length=5)
    nombre = models.CharField(max_length=50)
    simbolo = models.CharField(max_length=5)

    def __str__(self):
        return self.nombre


class Cuenta(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    saldo_cuenta = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    documento_identidad = models.CharField(max_length=25)
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    correo = models.EmailField(max_length=100)
    saldo = models.DecimalField(max_digits=15, decimal_places=2)
    contrasena = models.CharField(max_length=20)
    telefono = models.BigIntegerField()
    imagen_perfil = models.BinaryField(null=True, blank=True)
    id_moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    id_cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno}"


class MetaAhorro(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_limite = models.DateTimeField()
    monto_objetivo = models.DecimalField(max_digits=15, decimal_places=2)
    frecuencia_aporte = models.DateTimeField()
    descripcion = models.CharField(max_length=255)
    nombre = models.CharField(max_length=50)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class MoldeAhorro(models.Model):
    nombre = models.CharField(max_length=50)
    porcentaje_ahorro = models.DecimalField(max_digits=3, decimal_places=2)
    id_meta_ahorro = models.ForeignKey(MetaAhorro, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Movimiento(models.Model):
    tipo = models.CharField(max_length=25)
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    fecha_movimiento = models.DateTimeField()
    descripcion = models.CharField(max_length=300)
    id_cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo} - {self.monto}"


class Reporte(models.Model):
    tipo_reporte = models.CharField(max_length=25)
    fecha_creacion = models.DateTimeField()
    fecha_cierre = models.DateTimeField()
    id_cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)

    def __str__(self):
        return self.tipo_reporte
