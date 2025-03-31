# crearemos un formulario apartir de la tabla creada en models

from django import forms
from .models import Task # importamos el modelo de tarea

# formulario para crear tarea
class TaskForm(forms.ModelForm):
    class Meta:
        model= Task
        fields=['title','description','important']
        widgets={
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder':'Write a title'}),
            'description': forms.Textarea(attrs={'class': 'form-control','placeholder':'Write a description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
            
        }