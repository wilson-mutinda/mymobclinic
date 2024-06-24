from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, "blog/home.html")

def symptoms(request):
    return render(request, "blog/symptoms.html")
