from django.shortcuts import render
from django.http import HttpResponse

""" Url App ANALISIS_REPORTES """
app_name = "analisis_reportes"
def reports(request):
    return render(request, "analisis_reportes/reports.html")