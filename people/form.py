import re
from django import forms
from .models import People


class PersonForm(forms.ModelForm):
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s'-]+", nombre):
            raise forms.ValidationError('El nombre solo puede contener letras, espacios, apóstrofes o guiones.')
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido', '').strip()
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s'-]+", apellido):
            raise forms.ValidationError('El apellido solo puede contener letras, espacios, apóstrofes o guiones.')
        return apellido

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip()
        if not re.fullmatch(r"[0-9+()\-\s]{7,20}", telefono):
            raise forms.ValidationError('El teléfono solo puede contener números, espacios, paréntesis, + o guiones.')
        return telefono

    def clean_correo(self):
        correo = self.cleaned_data.get('correo', '').strip()
        if correo and not re.fullmatch(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", correo):
            raise forms.ValidationError('Ingrese un correo electrónico válido.')
        return correo

    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad is not None and (edad < 1 or edad > 120):
            raise forms.ValidationError('La edad debe estar entre 1 y 120 años.')
        return edad

    def clean_urbanizacion(self):
        urbanizacion = self.cleaned_data.get('urbanizacion', '').strip()
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9\s.-]+", urbanizacion):
            raise forms.ValidationError('La urbanización solo puede contener letras, números, espacios, puntos o guiones.')
        return urbanizacion

    class Meta:
        model = People
        fields = [
            'nombre',
            'apellido',
            'telefono',
            'correo',
            'edad',
            'urbanizacion',
            'referido_por',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),

            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido'
            }),

            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono'
            }),

            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico'
            }),

            'edad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Edad',
                'min': '1',
                'max': '120'
            }),

            'urbanizacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Urbanización'
            }),

            'referido_por': forms.Select(attrs={
                'class': 'form-control'
            }),
        }