from django.shortcuts import render
from django.http import HttpResponse

def Index(request):
    Data = {
        "message" : "Mensaje enviado desde Django",
    }
    return render(request , 'index.html')

def Login(request):
    if(request.method == "POST"):
        username = request.POST.get("USERNAME")
        email = request.POST.get("EMAIL")
        password = request.POST.get("PASSWORD")

        return HttpResponse(f"Formulario recibido\nnombre de usuario{username}\ncorreo:{email}\ncontraseña{password}")
    return render(request , 'login.html')