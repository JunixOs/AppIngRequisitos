from django.shortcuts import render
from django.http import HttpResponse

""" Views App EDUCACION_FINANCIERA """
def calculators(request):
    tab = request.GET.get("tab", "savings")  # default tab
    result = None

    if request.method == "POST":
        if tab == "savings":
            try:
                initial = float(request.POST.get("initial", 0))
                monthly = float(request.POST.get("monthly", 0))
                rate = float(request.POST.get("rate", 0)) / 100
                years = int(request.POST.get("years", 0))
                months = years * 12
                future_value = initial * (1 + rate/12) ** months + monthly * (((1 + rate/12) ** months - 1) / (rate/12))
                result = round(future_value, 2)
            except:
                result = "Error en los valores ingresados"
        
        elif tab == "loan":
            try:
                amount = float(request.POST.get("amount", 0))
                rate = float(request.POST.get("rate", 0)) / 100
                years = int(request.POST.get("years", 0))
                months = years * 12
                monthly_rate = rate / 12
                payment = amount * monthly_rate / (1 - (1 + monthly_rate) ** -months)
                result = round(payment, 2)
            except:
                result = "Error en los valores ingresados"

    return render(request, "educacion_financiera/calculators.html", {
        "tab": tab,
        "result": result
    })

def courses(request):
    course_list = [
        {
            "title": "Fundamentos Financieros",
            "description": "Aprende los conceptos básicos para gestionar tus finanzas personales",
            "lessons": 8,
            "progress": 25,
            "button": "Continuar Curso"
        },
        {
            "title": "Fundamentos de Inversión",
            "description": "Conoce los fundamentos de la inversión y cómo hacer crecer tu dinero",
            "lessons": 6,
            "progress": 0,
            "button": "Comenzar Curso"
        },
        {
            "title": "Gestión de Deudas",
            "description": "Estrategias efectivas para manejar y reducir tus deudas",
            "lessons": 5,
            "progress": 60,
            "button": "Continuar Curso"
        },
        {
            "title": "Planificación para el Retiro",
            "description": "Planifica tu retiro y asegura tu futuro financiero",
            "lessons": 7,
            "progress": 0,
            "button": "Comenzar Curso"
        },
    ]
    return render(request, "educacion_financiera/courses.html", {"courses": course_list})
