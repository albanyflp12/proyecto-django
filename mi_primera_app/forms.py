from django import forms
from .models import Inscripcion, Curso, Tatuaje
from usuarios.models import Tatuador, EstiloTatuaje

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre', 'descripcion', 'duracion_semanas', 'fecha_inicio', 'activo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
        }



class TurnoTatuajeForm(forms.ModelForm):
    fecha_turno = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    estilo = forms.ModelChoiceField(
        queryset=EstiloTatuaje.objects.filter(creador__disponible=True),
        required=False,
        empty_label="Seleccione un estilo de tatuaje",
        label="Estilo de Tatuaje"
    )
    
    class Meta:
        model = Tatuaje
        fields = ['nombre', 'descripcion', 'fecha_turno', 'email_contacto', 'edad_cliente', 'estilo']


class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = []