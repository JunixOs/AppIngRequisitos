from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import MovimientoForm
""" Views App GESTION_FINANCIERA_BASICA """
def savings_goals(request):
    goals = [
        ("Emergency Fund", "$3000.00 / $5000.00", "60%", "December 30, 2023", "Emergency fund for unexpected expenses"),
        ("Vacation", "$800.00 / $2000.00", "40%", "October 14, 2023", "Summer beach vacation"),
        ("New Laptop", "$450.00 / $1200.00", "37.5%", "November 29, 2023", "Replace old laptop"),
    ]

    tips = [
        ("📂", "50/30/20 Rule", "Allocate 50% of income to needs, 30% to wants, and 20% to savings."),
        ("🌱", "Pay Yourself First", "Transfer money to savings as soon as you receive income."),
    ]

    return render(request, "gestion_financiera_basica/savings_goals.html", {
        "goals": goals,
        "tips": tips
    })

def transactions(request):
    filter_type = request.GET.get("filter", "all")

    all_transactions = [
        ("Internet Bill", "Jul 21, 2023", "Utilities", "-$150.00", "bg-teal-500"),
        ("Movie Night", "Jul 19, 2023", "Entertainment", "-$35.00", "bg-indigo-500"),
        ("Restaurant Dinner", "Jul 17, 2023", "Food & Dining", "-$60.00", "bg-yellow-500"),
        ("Freelance Work", "Jul 14, 2023", "Income", "+$200.00", "bg-teal-500"),
        ("Gas Bill", "Jul 9, 2023", "Utilities", "-$45.00", "bg-teal-500"),
        ("Grocery Shopping", "Jul 4, 2023", "Food & Dining", "-$120.00", "bg-yellow-500"),
        ("Rent Payment", "Jul 2, 2023", "Housing", "-$800.00", "bg-indigo-500"),
        ("Monthly Salary", "Jun 30, 2023", "Income", "+$2500.00", "bg-teal-500"),
    ]

    if filter_type == "income":
        transactions = [t for t in all_transactions if "+" in t[3]]
    elif filter_type == "expenses":
        transactions = [t for t in all_transactions if "-" in t[3]]
    else:
        transactions = all_transactions

    return render(request, "gestion_financiera_basica/transactions.html", {
        "transactions": transactions,
        "filter_type": filter_type,
    })

def agregar_movimiento(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transactions')  # nombre de la vista que muestra transacciones
    else:
        form = MovimientoForm()
    
    return render(request, 'gestion_financiera_basica/add_transaction.html', {'form': form})