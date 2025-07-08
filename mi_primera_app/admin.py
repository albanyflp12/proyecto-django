from django.contrib import admin

# Register your models here.

from .models import Familiar, Curso, Tatuaje

register_models = [Familiar, Curso, Tatuaje]

admin.site.register(register_models)