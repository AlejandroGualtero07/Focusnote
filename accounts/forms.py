from django import forms
from .models import Perfil


class PerfilForm(forms.ModelForm):
    """
    Formulario para editar el perfil de usuario.
    Permite modificar la foto de perfil y la información relevante.
    """
    class Meta:
        model = Perfil
        fields = ['foto_perfil', 'informacion_relevante']
        widgets = {
            'informacion_relevante': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Escribe información sobre ti...'
            }),
            'foto_perfil': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'foto_perfil': 'Foto de perfil',
            'informacion_relevante': 'Información relevante'
        }


