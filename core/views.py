from django.shortcuts import render

""" Views App CORE """

def Inicio(request):
    return render(request, 'core/index.html')

def dashboard(request):
    tab = request.GET.get("tab", "overview")

    savings_goals = [
        ("Emergency Fund", "$3000.00 / $5000.00", "60%", "December 30, 2023"),
        ("Vacation", "$800.00 / $2000.00", "40%", "October 14, 2023"),
        ("New Laptop", "$450.00 / $1200.00", "37.5%", "November 29, 2023"),
    ] if tab == "savings" else []

    return render(request, "core/dashboard.html", {
        "tab": tab,
        "savings_goals": savings_goals
    })

