from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Avatar(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='avatar')
    imagen = models.ImageField(upload_to='avatares')

    def __str__(self):
        return f"Avatar de {self.user.username}"
    
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class Profesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    especialidad = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    disponible = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.especialidad}"
    
class EstiloTatuaje(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    creador = models.ForeignKey('usuarios.Tatuador', on_delete=models.CASCADE, related_name='estilos_creados', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Tatuador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    especialidad = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.especialidad}"
    
class UserProfile(models.Model):
    USER_TYPES = (
        ('usuario', 'Usuario'),
        ('tatuador', 'Tatuador'),
        ('profesor', 'Profesor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=USER_TYPES)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, tipo='usuario')