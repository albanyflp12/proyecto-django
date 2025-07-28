from django.urls import path

from .views import CustomLoginView, CustomLogoutView, ProfileView, AvatarUpdateView, ProfileUpdateView, UsuarioRegisterView, ProfesorRegisterView, TatuadorRegisterView, register_home, perfil_redirect, dashboard_profesor, dashboard_tatuador, dashboard_usuario, turnos_tatuador, cancelar_turno_tatuador

urlpatterns = [
    
    path('register/', register_home, name='register-home'),
    path('register/usuario', UsuarioRegisterView.as_view(), name='register_usuario'),
    path('register/profesor', ProfesorRegisterView.as_view(), name='register_profesor'),
    path('register/tatuador', TatuadorRegisterView.as_view(), name='register_tatuador'),
    path('perfil/', perfil_redirect, name='perfil_redirect'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/usuario/', dashboard_usuario, name='dashboard_usuario'),
    path('dashboard/tatuador/', dashboard_tatuador, name='dashboard_tatuador'),
    path('tatuador/turnos/', turnos_tatuador, name='turnos_tatuador'),
    path('tatuador/turnos/cancelar/<int:turno_id>/', cancelar_turno_tatuador, name='cancelar_turno_tatuador'),
    path('dashboard/profesor/', dashboard_profesor, name='dashboard_profesor'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='edit_profile'),
    path('profile/avatar/', AvatarUpdateView.as_view(), name='avatar-update'),
]