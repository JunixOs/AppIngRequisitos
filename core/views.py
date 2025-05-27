from django.shortcuts import render


def Inicio(request):
    return render(request, 'core/index.html')

def Home(request):
    return render(request, 'core/home.html')