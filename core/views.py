from django.shortcuts import render

def index(request):
    return render(request, "core/index.html")

def lp(request):
    return render(request, "core/lp.html")
