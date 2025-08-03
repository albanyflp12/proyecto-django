# Proyecto Django

Este es un proyecto web desarrollado con Django como entrega final del curso de Python con Django. La aplicación permite gestionar cursos de tatuajes, perfiles de usuarios, turnos y mensajería interna entre usuarios.

# Funcionalidades principales

- Home y página "Acerca de mí".
- Registro y login de usuarios con distintos roles: Usuario, Profesor y Tatuador.
- Perfil editable con avatar, biografía, y cambio de contraseña.
- Sistema de cursos:
  - Profesores pueden crear, editar, eliminar y ver cursos con lista de estudiantes inscritos.
  - Usuarios pueden buscar cursos e inscribirse.
- Sistema de turnos para tatuajes:
  - Tatuadores pueden crear estilos y gestionar turnos solicitados.
  - Usuarios pueden ver tatuadores y pedir turnos.
- Navegación dinámica según tipo de usuario (dashboard personalizado).
- Protección de vistas con login y validaciones de tipo de usuario.

# Crear entorno virtual e ingresar a pagina

En MAC: source venv/bin/activate
En Windows: venv\Scripts\Activate.ps1

Github: https://github.com/albanyflp12/proyecto-django

Runserver en MAC: python3 manage.py runserver
Runserver en windows python manage.py runserver

URL: http://127.0.0.1:8000/

# Link a mi video: