from django.shortcuts import render

def home(request):
    # El argumento de 'render' debe ser 'crudApp/home.html', no 'home.html' si sigues la convención estándar.
    return render(request, 'crudApp/home.html')