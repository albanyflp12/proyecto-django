from django.shortcuts import render
from .models import Familiar

# Create your views here.
from django.http import HttpResponse

def saludo(request):
    return HttpResponse("Hola, mundo!")

def saludo_con_template(request):
    return render(request, 'mi_primera_app/saludo.html')

def crear_familiar(request, nombre):
    if nombre is not None:

        nuevo_familiar = Familiar(
            nombre=nombre,
            apellido="ApellidoEjemplo",
            edad=30,
            fecha_nacimiento="1995-12-07",
            parentesco="Primo"
        )
        nuevo_familiar.save()
    return render(request, "mi_primera_app/crear_familiar.html", {"nombre": nombre})