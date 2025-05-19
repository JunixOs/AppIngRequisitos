from django.shortcuts import render
from django.http import HttpResponse

def Index(request):
    Data = {
        "message" : "Mensaje enviado desde Django",
    }
    return render(request , 'index.html')

def Login(request):
    if(request.method == "POST"):
        email = request.POST.get("EMAIL")
        password = request.POST.get("PASSWORD")

        return HttpResponse(f"Formulario recibido\ncorreo:{email}\ncontraseña{password}")
    return render(request , 'login.html')

def Register(request):
    if(request.method == "POST"):
        username = request.POST.get("USERNAME")
        email = request.POST.get("EMAIL")
        password = request.POST.get("PASSWORD")

        return HttpResponse(f"Recibido\n{username}\n{email}\n{password}")
    return render(request , 'register.html')

def Ayuda(request):
    return render(request, 'ayuda.html')


def Contacto(request):
    return render(request, 'contacto.html')