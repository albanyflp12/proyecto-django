from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .models import Familiar, Curso, Tatuaje, Inscripcion
from usuarios.models import Usuario, Tatuador, Profesor

from .forms import CursoForm, TurnoTatuajeForm, TatuadorDataForm

from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse

def home(request):
    return render(request, 'mi_primera_app/home.html')

def tattoo_style(request):
    return render(request, 'mi_primera_app/tattoo_style.html')

def acerca_de(request):
    return render(request, 'mi_primera_app/acerca_de.html')

def saludo(request):
    return HttpResponse("Hola, mundo!")

def saludo_con_template(request):
    return render(request, 'mi_primera_app/saludo.html')

def crear_familiar(request, nombre):
    if nombre is not None:

        nuevo_familiar = Familiar(
            nombre=nombre,
            apellido="ApellidoEjemplo",
            edad=30,
            fecha_nacimiento="1995-12-07",
            parentesco="Primo"
        )
        nuevo_familiar.save()
    return render(request, "mi_primera_app/crear_familiar.html", {"nombre": nombre})


@login_required
def crear_curso(request):
    if request.method == "POST":
        form = CursoForm(request.POST)
        if form.is_valid():
            profesor = Profesor.objects.get(user=request.user)  # obtenemos el profesor logueado

            nuevo_curso = Curso(
                nombre=form.cleaned_data['nombre'],
                descripcion=form.cleaned_data['descripcion'],
                duracion_semanas=form.cleaned_data['duracion_semanas'],
                fecha_inicio=form.cleaned_data['fecha_inicio'],
                activo=form.cleaned_data['activo'],
                profesor=profesor  # lo asignamos al curso
            )
            nuevo_curso.save()
            return redirect('dashboard_profesor')  # redirige al dashboard del profesor
    else:
        form = CursoForm()
    
    return render(request, "mi_primera_app/crear_curso.html", {"form": form})

@login_required
def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    inscriptos = curso.inscripciones.select_related('usuario')

    return render(request, "mi_primera_app/detalle_curso.html", {
        "curso": curso,
        "inscriptos": inscriptos,
    })

@login_required
def inscribirse_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    usuario = get_object_or_404(Usuario, user=request.user)

    if Inscripcion.objects.filter(usuario=usuario, curso=curso).exists():
        messages.warning(request, "Ya estás inscrito en este curso.")
    else:
        Inscripcion.objects.create(usuario=usuario, curso=curso)
        messages.success(request, "Te has inscrito correctamente.")

    return redirect('detalle_curso', curso_id=curso.id)  # ajustá este nombre a tu URL
    
def cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'mi_primera_app/cursos.html', {'cursos': cursos})

def buscar_cursos(request):
    if request.method == 'GET':
        nombre = request.GET.get('nombre', '')
        cursos = Curso.objects.filter(nombre__icontains=nombre)
        return render(request, 'mi_primera_app/cursos.html', {'cursos': cursos, 'nombre': nombre})

@login_required
def crear_turno_tatuaje(request):
    if request.method == "POST":
        form = TurnoTatuajeForm(request.POST)
        if form.is_valid():
            nuevo_tatuaje = Tatuaje(
                nombre=form.cleaned_data['nombre'],
                descripcion=form.cleaned_data['descripcion'],
                fecha_turno=form.cleaned_data['fecha_turno'],
                email_contacto=form.cleaned_data['email_contacto'],
                edad_cliente=form.cleaned_data['edad_cliente'],
                tatuador=form.cleaned_data.get('tatuador')  # asignamos el FK aquí
            )
            nuevo_tatuaje.save()
            return redirect('home')
    else:
        form = TurnoTatuajeForm()
    return render(request, "mi_primera_app/crear_turno_tatuaje.html", {"form": form})

@login_required
def lista_turnos_tatuaje(request):
    turnos = Tatuaje.objects.filter(email_contacto=request.user.email).order_by('fecha_turno')
    return render(request, 'mi_primera_app/lista_turnos_tatuaje.html', {'turnos': turnos})

@login_required
def cancelar_turno_tatuaje(request, turno_id):
    turno = get_object_or_404(Tatuaje, id=turno_id, email_contacto=request.user.email)
    if request.method == 'POST':
        turno.delete()
        return redirect('lista_turnos_tatuaje')
    return render(request, 'mi_primera_app/cancelar_turno_tatuaje.html', {'turno': turno})

class TatuadorListView(ListView):
    model = Tatuador
    template_name = 'mi_primera_app/listar_tatuadores.html'
    context_object_name = 'tatuadores'

class TatuadorCreateView(CreateView):
    model = Tatuador
    form_class = TatuadorDataForm
    template_name = 'mi_primera_app/crear_tatuador.html'
    success_url = reverse_lazy('listar-tatuadores')

class TatuadorDetailView(DetailView):
    model = Tatuador
    template_name = 'mi_primera_app/detalle_tatuador.html'
    context_object_name = 'tatuador'

class TatuadorUpdateView(UpdateView):
    model = Tatuador
    form_class = TatuadorDataForm
    template_name = 'mi_primera_app/crear_tatuador.html'
    success_url = reverse_lazy('listar-tatuadores')

class TatuadorDeleteView(DeleteView):
    model = Tatuador
    template_name = 'mi_primera_app/eliminar_tatuador.html'
    success_url = reverse_lazy('listar-tatuadores')
