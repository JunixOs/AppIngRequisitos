from django.db import models


# Create your models here.
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
    id_moneda = models.ForeignKey("cuentas.Moneda", on_delete=models.CASCADE)
    id_cuenta = models.ForeignKey("cuentas.Cuenta", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno}"
