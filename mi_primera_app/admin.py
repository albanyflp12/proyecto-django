from django.contrib import admin

from .models import Familiar, Curso, Tatuaje, Inscripcion

register_models = [Familiar, Curso, Tatuaje, Inscripcion]

admin.site.register(register_models)