from django.shortcuts import render

def home(request):
    return render(request, 'backend/index.html')


def register(request):
    return render(request, 'backend/register.html')

def login(request):
    return render(request, 'backend/login.html')
