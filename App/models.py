from django.db import models
from django.contrib.auth.models import AbstractUser

class Moneda(models.Model):
    codigo = models.CharField(max_length=5 , unique=True) # PEN , USD , COL , EUR , etc...
    nombre = models.CharField(max_length=50) # Nuevos Soles , Dolares Estadounidenses , Pesos Colombianos , Euros , etc
    simbolo = models.CharField(max_length=5) # S/. , $. , , e

    def __str__(self):
        return f"Codigo: {self.codigo}\nNombre de moneda: {self.nombre}\nSimbolo: {self.simbolo}"

class Usuario(AbstractUser):
    nombres = models.CharField(max_length=80 , null=False)
    apellido_materno = models.CharField(max_length=50 , null=False)
    apellido_paterno = models.CharField(max_length=50 , null=False)
    correo = models.EmailField(max_length=100 , null=False)
    telefono = models.IntegerField(max_length=30 , null=False)
    DNI = models.IntegerField(max_length=50 , null=False)

    saldo = models.DecimalField(max_digits=15 , decimal_places=2 , default=0.00)

    moneda = models.ForeignKey(Moneda , on_delete=models.SET_NULL , null=True)

    imagen_de_perfil = models.ImageField(upload_to="profiles/" , blank=True , null=True)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombres' , 'apellido_materno' , 'apellido_paterno']

    def __str__(self):
        return f"Nombres: {self.nombres}\nApellido paterno: {self.apellido_paterno}\nApellido materno: {self.apellido_materno}"