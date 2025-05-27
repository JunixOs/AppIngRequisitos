from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(request):
    return HttpResponse("Bienvenido a la app del modulo Gestion de Usuarios. Estas en login")