from django.db import models

# Create your models here.
class Familiar(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    edad = models.IntegerField()
    fecha_nacimiento =  models.DateField()
    parentesco = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.parentesco}) - Edad: {self.edad}, Nacido el: {self.fecha_nacimiento}"


class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    duracion_semanas = models.IntegerField(default=True)
    fecha_inicio = models.DateField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
from django.db import models

class Tatuaje(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_turno = models.DateField()
    email_contacto = models.EmailField()
    edad_cliente = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} - {self.fecha_turno}"
    

class Auto(models.Model):
    modelo = models.CharField(max_length=20)
    marca = models.CharField(max_length=20)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.marca} {self.modelo}'