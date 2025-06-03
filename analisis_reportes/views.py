from django.shortcuts import render
from django.http import HttpResponse

""" Url App ANALISIS_REPORTES """
def reports(request):
    return render(request, "analisis_reportes/reports.html")