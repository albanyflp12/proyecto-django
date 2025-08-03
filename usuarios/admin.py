from django.contrib import admin

from .models import Avatar, Usuario, Profesor, Tatuador, EstiloTatuaje, UserProfile

register_models = [Avatar, Usuario, Profesor, Tatuador, EstiloTatuaje, UserProfile]

admin.site.register(register_models)