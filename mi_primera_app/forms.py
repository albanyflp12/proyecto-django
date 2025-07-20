from django import forms
from .models import Auto

class CursoForm(forms.Form):
    nombre = forms.CharField()
    descripcion = forms.CharField(widget=forms.Textarea, required=False)
    duracion_semanas = forms.IntegerField(min_value=1, initial=4)
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    activo = forms.BooleanField(required=False, initial=True)



class TatuajeForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100)
    descripcion = forms.CharField(widget=forms.Textarea,required=False)
    fecha_turno = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    email_contacto = forms.EmailField()
    edad_cliente = forms.IntegerField(min_value=18, initial=18)


class AutoForm(forms.ModelForm):
    class Meta:
        model = Auto
        fields = ['modelo', 'marca', 'descripcion']
        