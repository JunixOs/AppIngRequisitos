from django.shortcuts import render

def Index(request):
    Data = {
        "message" : "Mensaje enviado desde Django",
    }
    return render(request , 'index.html')

def Login(request):
    return render(request , 'login.html')