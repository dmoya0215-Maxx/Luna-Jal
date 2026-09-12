import re
from django import forms
from .models import People, URBANIZACIONES


class PersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Al editar, excluir a la persona actual de "Referido por"
        if self.instance.pk is not None:
            self.fields['referido_por'].queryset = People.objects.exclude(
                id=self.instance.pk
            )

        # Urbanización: Select con las opciones definidas.
        # Se permite conservar valores históricos que no estén en la lista.
        opciones_urbanizacion = [('', 'Seleccione una urbanización')] + list(URBANIZACIONES)
        valor_actual = self.instance.urbanizacion if self.instance else ''
        if valor_actual and valor_actual not in dict(URBANIZACIONES):
            opciones_urbanizacion.append((valor_actual, valor_actual))

        self.fields['urbanizacion'] = forms.ChoiceField(
            choices=opciones_urbanizacion,
            required=True,
            error_messages={
                'required': 'Seleccione una urbanización.',
                'invalid_choice': 'Seleccione una urbanización válida.',
            },
            widget=forms.Select(attrs={'class': 'form-control custom-select'}),
        )

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
        correo = (self.cleaned_data.get('correo') or '').strip()
        if correo and not re.fullmatch(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", correo):
            raise forms.ValidationError('Ingrese un correo electrónico válido.')
        return correo or None

    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad is not None and (edad < 1 or edad > 120):
            raise forms.ValidationError('La edad debe estar entre 1 y 120 años.')
        return edad

    def clean_referido_por(self):
        referido_por = self.cleaned_data.get('referido_por')
        if (
            referido_por is not None
            and self.instance.pk is not None
            and referido_por.pk == self.instance.pk
        ):
            raise forms.ValidationError(
                'Una persona no puede referirse a sí misma.'
            )
        return referido_por

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

            'referido_por': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
