from django.urls import path

from .views import saludo, saludo_con_template, crear_familiar, home, crear_curso, crear_tatuaje, buscar_cursos, cursos

urlpatterns = [
    path('', home, name='home'),
    path('hola-mundo/', saludo),
    path('hola-mundo-template/', saludo_con_template),
    path('crear-familiar/<str:nombre>/', crear_familiar),
    path('crear-curso/', crear_curso, name='crear-curso'),
    path('crear-tatuaje/', crear_tatuaje, name='crear-tatuaje'),
    path('cursos/', cursos, name='cursos'),
    path('cursos/buscar', buscar_cursos, name='buscar-cursos'),
]