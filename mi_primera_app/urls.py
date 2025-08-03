from django.urls import path

from .views import (saludo, saludo_con_template, crear_familiar, 
                    home, acerca_de, tattoo_style, crear_curso, crear_turno_tatuaje, lista_turnos_tatuaje, buscar_cursos, cursos, inscribirse_curso, cancelar_turno_tatuaje, detalle_curso, cancelar_inscripcion, 
                    TatuadorListView, TatuadorDetailView, CursoDeleteView, CursoUpdateView, cursos_profesor, editar_turno_tatuaje, detalle_turno_tatuaje)

urlpatterns = [
    path('', home, name='home'),
    path('acerca-de/', acerca_de, name='acerca_de'),
    path('tattoo-style/', tattoo_style, name='tattoo_style'),
    path('hola-mundo/', saludo),
    path('hola-mundo-template/', saludo_con_template),
    path('crear-familiar/<str:nombre>/', crear_familiar),
    path('crear-curso/', crear_curso, name='crear-curso'),
    path("cursos/<int:curso_id>/", detalle_curso, name="detalle_curso"),
    path('curso/<int:curso_id>/cancelar/', cancelar_inscripcion, name='cancelar_inscripcion'),
    path('cursos/', cursos, name='cursos'),
    path('cursos/profesor/', cursos_profesor, name='cursos_profesor'),
    path('cursos/buscar', buscar_cursos, name='buscar-cursos'),
    path('curso/<int:curso_id>/inscribirse/', inscribirse_curso, name='inscribirse_curso'),
    path('crear-turno-tatuaje/', crear_turno_tatuaje, name='crear-turno-tatuaje'),
    path('turno/editar/<int:turno_id>/', editar_turno_tatuaje, name='editar_turno_tatuaje'),
    path('turno/detalle/<int:turno_id>/', detalle_turno_tatuaje, name='detalle_turno_tatuaje'),
    path('turnos/', lista_turnos_tatuaje, name='lista-turnos-tatuaje'),
    path('turnos/cancelar/<int:turno_id>/', cancelar_turno_tatuaje, name='cancelar_turno_tatuaje'),
    

    # urls con vistas basadas en clase
    path('curso/<int:pk>/editar/', CursoUpdateView.as_view(), name='editar_curso'),
    path('curso/<int:pk>/eliminar/', CursoDeleteView.as_view(), name='eliminar_curso'),
    path('listar-tatuadores/', TatuadorListView.as_view(), name='listar-tatuadores'),
    path('detalle-tatuador/<int:pk>/', TatuadorDetailView.as_view(), name='detalle-tatuador'),
]