from django.shortcuts import render
from django.http import HttpResponse

""" Views App CUENTAS """
def profile(request):
    tab = request.GET.get("tab", "general")
    return render(request, "cuentas/profile.html", {"tab": tab})

def settings(request):
    return render(request, "cuentas/settings.html")