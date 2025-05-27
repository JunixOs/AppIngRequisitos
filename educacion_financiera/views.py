from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def Ayuda(request):
    return render(request, 'educacion_financiera/ayuda.html')

def Contacto(request):
    return render(request, 'educacion_financiera/contacto.html')