from django.urls import path

from .views import (saludo, saludo_con_template, crear_familiar, 
                    home, acerca_de, tattoo_style, crear_curso, crear_turno_tatuaje, lista_turnos_tatuaje, buscar_cursos, cursos, inscribirse_curso, cancelar_turno_tatuaje, detalle_curso, 
                    TatuadorCreateView, TatuadorListView, TatuadorDetailView, TatuadorUpdateView, TatuadorDeleteView)

urlpatterns = [
    path('', home, name='home'),
    path('acerca-de/', acerca_de, name='acerca_de'),
    path('tattoo-style/', tattoo_style, name='tattoo_style'),
    path('hola-mundo/', saludo),
    path('hola-mundo-template/', saludo_con_template),
    path('crear-familiar/<str:nombre>/', crear_familiar),
    path('crear-curso/', crear_curso, name='crear-curso'),
    path("cursos/<int:curso_id>/", detalle_curso, name="detalle_curso"),
    path('cursos/', cursos, name='cursos'),
    path('cursos/buscar', buscar_cursos, name='buscar-cursos'),
    path('curso/<int:curso_id>/inscribirse/', inscribirse_curso, name='inscribirse_curso'),
    path('crear-turno-tatuaje/', crear_turno_tatuaje, name='crear-turno-tatuaje'),
    path('turnos/', lista_turnos_tatuaje, name='lista-turnos-tatuaje'),
    path('turnos/cancelar/<int:turno_id>/', cancelar_turno_tatuaje, name='cancelar_turno_tatuaje'),
    

    # urls con vistas basadas en clase

    path('listar-tatuadores/', TatuadorListView.as_view(), name='listar-tatuadores'),
    path('crear-tatuador/', TatuadorCreateView.as_view(), name='crear-tatuador'),
    path('detalle-tatuador/<int:pk>/', TatuadorDetailView.as_view(), name='detalle-tatuador'),
    path('editar-tatuador/<int:pk>/', TatuadorUpdateView.as_view(), name='editar-tatuador'),
    path('eliminar-tatuador/<int:pk>/', TatuadorDeleteView.as_view(), name='eliminar-tatuador'),
]