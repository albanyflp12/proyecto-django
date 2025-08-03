from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .models import Familiar, Curso, Tatuaje, Inscripcion
from usuarios.models import Usuario, Tatuador, Profesor, EstiloTatuaje

from .forms import CursoForm, TurnoTatuajeForm

from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse

def home(request):
    return render(request, 'mi_primera_app/home.html')

def tattoo_style(request):
    estilos = EstiloTatuaje.objects.prefetch_related('creador')  
    return render(request, 'mi_primera_app/tattoo_style.html', {
        'estilos': estilos,
    })

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
            curso = form.save(commit=False)
            profesor = Profesor.objects.get(user=request.user)
            curso.profesor = profesor
            curso.save()
            return redirect('dashboard_profesor')
    else:
        form = CursoForm()

    return render(request, "mi_primera_app/crear_curso.html", {"form": form})

@login_required
def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    puede_ver_inscriptos = False
    ya_inscripto = False

    if hasattr(request.user, 'userprofile') and request.user.userprofile.tipo == 'profesor':
        profesor = get_object_or_404(Profesor, user=request.user)
        puede_ver_inscriptos = (curso.profesor == profesor)

    if hasattr(request.user, 'userprofile') and request.user.userprofile.tipo == 'usuario':
        usuario = get_object_or_404(Usuario, user=request.user)
        ya_inscripto = Inscripcion.objects.filter(usuario=usuario, curso=curso).exists()

    inscriptos = curso.inscripciones.select_related('usuario')

    return render(request, "mi_primera_app/detalle_curso.html", {
        "curso": curso,
        "inscriptos": inscriptos,
        "ya_inscripto": ya_inscripto,
        "puede_ver_inscriptos": puede_ver_inscriptos,
    })
    
class CursoUpdateView(UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'mi_primera_app/editar_curso.html'  

    def get_success_url(self):
        return reverse_lazy('dashboard_profesor')

class CursoDeleteView(DeleteView):
    model = Curso
    template_name = 'mi_primera_app/eliminar_curso.html'  
    success_url = reverse_lazy('dashboard_profesor')

@login_required
def cursos_profesor(request):
    profesor = request.user.profesor  
    cursos = Curso.objects.filter(profesor=profesor)
    return render(request, 'mi_primera_app/cursos_profesor.html', {'cursos': cursos})

@login_required
def inscribirse_curso(request, curso_id):
    
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.tipo != 'usuario':
        messages.error(request, 'Solo los usuarios pueden inscribirse a cursos.')
        return redirect('cursos')

    curso = get_object_or_404(Curso, id=curso_id)
    usuario = get_object_or_404(Usuario, user=request.user)

    if Inscripcion.objects.filter(usuario=usuario, curso=curso).exists():
        messages.warning(request, "Ya estás inscrito en este curso.")
    else:
        Inscripcion.objects.create(usuario=usuario, curso=curso)
        messages.success(request, "Te has inscrito correctamente.")

    return redirect('detalle_curso', curso_id=curso.id)

def cancelar_inscripcion(request, curso_id):
    usuario = get_object_or_404(Usuario, user=request.user)
    curso = get_object_or_404(Curso, id=curso_id)
    inscripcion = Inscripcion.objects.filter(usuario=usuario, curso=curso).first()

    if inscripcion:
        inscripcion.delete()
        messages.success(request, "Te has dado de baja del curso correctamente.")
    else:
        messages.error(request, "No estás inscrito en este curso.")

    return redirect('dashboard_usuario')
    
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
    if request.method == 'POST':
        form = TurnoTatuajeForm(request.POST)
        if form.is_valid():
            turno = form.save(commit=False)
            estilo = turno.estilo
            if estilo:
                tatuadores = Tatuador.objects.filter(estilos_creados__id=estilo.id, disponible=True)
                if tatuadores.exists():
                    turno.tatuador = tatuadores.first()
            turno.save()
            return redirect('dashboard_usuario')
    else:
        form = TurnoTatuajeForm()
    return render(request, 'mi_primera_app/crear_turno_tatuaje.html', {'form': form})


@login_required
def detalle_turno_tatuaje(request, turno_id):
    turno = get_object_or_404(Tatuaje, id=turno_id, email_contacto=request.user.usuario.email)

    return render(request, 'mi_primera_app/detalle_turno_tatuaje.html', {
        'turno': turno,
    })

def editar_turno_tatuaje(request, turno_id):
    turno = get_object_or_404(Tatuaje, id=turno_id)

    if request.method == 'POST':
        form = TurnoTatuajeForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            messages.success(request, "Turno actualizado correctamente.")
            return redirect('dashboard_usuario')
    else:
        form = TurnoTatuajeForm(instance=turno)

    return render(request, 'mi_primera_app/editar_turno_tatuaje.html', {'form': form})

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

class TatuadorDetailView(DetailView):
    model = Tatuador
    template_name = 'mi_primera_app/detalle_tatuador.html'
    context_object_name = 'tatuador'

