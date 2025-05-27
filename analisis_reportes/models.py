from django.db import models

# Create your models here.
class Reporte(models.Model):
    tipo_reporte = models.CharField(max_length=25)
    fecha_creacion = models.DateTimeField()
    fecha_cierre = models.DateTimeField()
    id_cuenta = models.ForeignKey("cuentas.Cuenta", on_delete=models.CASCADE)

    def __str__(self):
        return self.tipo_reporte
