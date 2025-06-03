from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
@login_required(login_url='login')
def Index(request):
    Data = {
        "message" : "Mensaje enviado desde Django",
    }
    return render(request , 'index.html')

def Login(request):
    if request.method == "POST":
        email = request.POST.get("EMAIL")
        password = request.POST.get("PASSWORD")
        # Aquí deberías validar usuario y contraseña
        # Por simplicidad asumimos que está OK y redirigimos:
        return redirect('dashboard')  # o 'index' si tienes así la url
    return render(request, 'usuarios/login.html')

def Register(request):
    if(request.method == "POST"):
        username = request.POST.get("USERNAME")
        email = request.POST.get("EMAIL")
        password = request.POST.get("PASSWORD")

        return HttpResponse(f"Recibido\n{username}\n{email}\n{password}")
    return render(request , 'usuarios/register.html')