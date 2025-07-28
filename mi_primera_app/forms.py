from django import forms
from .models import Inscripcion
from usuarios.models import Tatuador

class CursoForm(forms.Form):
    nombre = forms.CharField()
    descripcion = forms.CharField(widget=forms.Textarea, required=False)
    duracion_semanas = forms.IntegerField(min_value=1, initial=4)
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    activo = forms.BooleanField(required=False, initial=True)



class TurnoTatuajeForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100)
    descripcion = forms.CharField(widget=forms.Textarea, required=False)
    fecha_turno = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    email_contacto = forms.EmailField()
    edad_cliente = forms.IntegerField(min_value=18, initial=18)
    tatuador = forms.ModelChoiceField(
        queryset=Tatuador.objects.filter(disponible=True),
        required=False,
        empty_label="Seleccione un tatuador",
        label="Tatuador"
    )

class TatuadorDataForm(forms.ModelForm):
    class Meta:
        model = Tatuador
        fields = [
            'nombre',
            'especialidad',
            'disponible',  
            'email'        
        ]

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = []