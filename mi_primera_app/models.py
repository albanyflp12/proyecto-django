from django.db import models
from usuarios.models import Usuario, Profesor, Tatuador

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
    descripcion = models.TextField()
    duracion_semanas = models.IntegerField()
    fecha_inicio = models.DateField()
    activo = models.BooleanField(default=True)
    profesor = models.ForeignKey(
        Profesor,
        on_delete=models.CASCADE,
        related_name='cursos',
        null=True,       
        blank=True       
    )

    def __str__(self):
        return self.nombre

class Tatuaje(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(default='Sin descripción disponible')
    fecha_turno = models.DateField()
    email_contacto = models.EmailField()
    edad_cliente = models.IntegerField()
    tatuador = models.ForeignKey(Tatuador, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.fecha_turno}"
    

class Inscripcion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='inscripciones')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'curso')

    def __str__(self):
        return f"{self.usuario.nombre} inscrito en {self.curso.nombre}"