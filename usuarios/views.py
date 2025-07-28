from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

from django.core.exceptions import ObjectDoesNotExist
from .forms import UsuarioForm, ProfesorForm, TatuadorRegisterForm, AvatarForm, ProfileUpdateForm
from django.views import View
from .models import Avatar, Usuario, Profesor, Tatuador, UserProfile
from mi_primera_app.models import Curso, Tatuaje, Inscripcion
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .decorators import user_tipo_requerido
    
class UsuarioRegisterView(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/register_usuario.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        
        Usuario.objects.create(
            user=user,
            nombre=f"{user.first_name} {user.last_name}",
            email=user.email
        )
        
        UserProfile.objects.update_or_create(user=user, defaults={'tipo': 'usuario'})

        login(self.request, user)
        return redirect(self.success_url)


class ProfesorRegisterView(CreateView):
    model = Profesor
    form_class = ProfesorForm
    template_name = 'usuarios/register_profesor.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        
        Profesor.objects.create(
            user=user,
            nombre=f"{user.first_name} {user.last_name}",
            email=user.email,
            especialidad=form.cleaned_data.get('especialidad', ''),
            descripcion=form.cleaned_data.get('descripcion', ''),
            disponible=True
        )
        
        UserProfile.objects.update_or_create(user=user, defaults={'tipo': 'profesor'})

        login(self.request, user)
        return redirect(self.success_url)


class TatuadorRegisterView(CreateView):
    model = Tatuador
    form_class = TatuadorRegisterForm
    template_name = 'usuarios/register_tatuador.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        
        Tatuador.objects.create(
            user=user,
            nombre=f"{user.first_name} {user.last_name}",
            email=user.email,
            especialidad=form.cleaned_data.get('especialidad', ''),
            descripcion=form.cleaned_data.get('descripcion', ''),
            disponible=True
        )
        
        UserProfile.objects.update_or_create(user=user, defaults={'tipo': 'tatuador'})

        login(self.request, user)
        return redirect(self.success_url)


@login_required
def turnos_tatuador(request):
    tatuador = get_object_or_404(Tatuador, user=request.user)
    turnos = Tatuaje.objects.filter(tatuador=tatuador).order_by('fecha_turno')

    return render(request, 'usuarios/turnos_tatuador.html', {'turnos': turnos})


@login_required
def cancelar_turno_tatuador(request, turno_id):
    tatuador = get_object_or_404(Tatuador, user=request.user)
    turno = get_object_or_404(Tatuaje, id=turno_id, tatuador=tatuador)

    if request.method == 'POST':
        turno.delete()
        return redirect('turnos_tatuador')

    return render(request, 'usuarios/cancelar_turno_tatuador.html', {'turno': turno})
    
def register_home(request):
    return render(request, 'usuarios/register_home.html')

@login_required
@user_tipo_requerido('usuario')
def dashboard_usuario(request):
    try:
        usuario = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        messages.error(request, "No tienes perfil de Usuario.")
        return redirect('perfil_redirect')

    cursos_inscritos = Curso.objects.filter(inscripciones__usuario=usuario)
    citas_agendadas = Tatuaje.objects.filter(email_contacto=usuario.email)

    context = {
        'cursos_inscritos': cursos_inscritos,
        'citas_agendadas': citas_agendadas,
    }
    return render(request, 'usuarios/dashboard_usuario.html', context)

@user_tipo_requerido('tatuador')
@login_required
def dashboard_tatuador(request):
    tatuador = Tatuador.objects.get(user=request.user)
    estilos_inscritos = [tatuador.especialidad]  # Asumiendo que se inscribe por especialidad
    citas_asignadas = Tatuaje.objects.filter(descripcion__icontains=tatuador.especialidad)

    context = {
        'estilos_inscritos': estilos_inscritos,
        'citas_asignadas': citas_asignadas,
    }
    return render(request, 'usuarios/dashboard_tatuador.html', context)

@user_tipo_requerido('profesor')
@login_required
def dashboard_profesor(request):
    profesor = Profesor.objects.get(user=request.user)
    cursos_impartidos = Curso.objects.filter(profesor=profesor)

    cursos_con_alumnos = {}
    for curso in cursos_impartidos:
        alumnos = Usuario.objects.filter(inscripciones__curso=curso).distinct()
        cursos_con_alumnos[curso] = alumnos

    context = {
        'cursos_impartidos': cursos_impartidos,
        'cursos_con_alumnos': cursos_con_alumnos,
    }
    return render(request, 'usuarios/dashboard_profesor.html', context)

def perfil_redirect(request):
    user = request.user
    print("DEBUG: user autenticado:", user)
    print("DEBUG: user.id:", user.id)

    try:
        profile = UserProfile.objects.get(user=user)
        print("DEBUG - tipo:", profile.tipo)
    except ObjectDoesNotExist:
        print("DEBUG - No se encontró perfil")
        return redirect('home')

    if profile.tipo == 'usuario':
        print("Redirect a dashboard_usuario")
        return redirect('dashboard_usuario')
    elif profile.tipo == 'profesor':
        print("Redirect a dashboard_profesor")
        return redirect('dashboard_profesor')
    elif profile.tipo == 'tatuador':
        print("Redirect a dashboard_tatuador")
        return redirect('dashboard_tatuador')
    else:
        return redirect('home')
    
class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'

    def get_success_url(self):
        # Redirige a perfil_redirect que a su vez redirige al dashboard
        return reverse_lazy('perfil_redirect')
    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'usuarios/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user
    
class AvatarUpdateView(LoginRequiredMixin ,UpdateView):
    model = Avatar
    form_class = AvatarForm
    template_name = 'usuarios/avatar_form.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        avatar, created = Avatar.objects.get_or_create(user=self.request.user)
        return avatar
    
class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = "usuarios/edit_profile.html"
    success_url = reverse_lazy("profile")

    def get(self, request, *args, **kwargs):
        user_form = ProfileUpdateForm(instance=request.user)
        avatar, _ = Avatar.objects.get_or_create(user=request.user)
        avatar_form = AvatarForm(instance=avatar)
        password_form = PasswordChangeForm(request.user)
        context = {
            "user_form": user_form,
            "avatar_form": avatar_form,
            "password_form": password_form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        user_form = ProfileUpdateForm(request.POST, instance=request.user)
        avatar, _ = Avatar.objects.get_or_create(user=request.user)
        avatar_form = AvatarForm(request.POST, request.FILES, instance=avatar)
        password_form = PasswordChangeForm(request.user, request.POST)

        if "update_profile" in request.POST:
            if user_form.is_valid() and avatar_form.is_valid():
                user_form.save()
                avatar_form.save()
                messages.success(request, "Perfil actualizado exitosamente")
                return redirect(self.success_url)
            else:
                messages.error(request, "Error al actualizar el perfil")
        elif "change_password" in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Contraseña actualizada exitosamente")
                return redirect(self.success_url)
            else:
                messages.error(request, "Error al cambiar la contraseña")
        
        context = {
            "user_form": user_form,
            "avatar_form": avatar_form,
            "password_form": password_form,
        }
        return render(request, self.template_name, context)