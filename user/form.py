import re
from django import forms
from django.utils import timezone
from .models import User

class UserForm(forms.ModelForm):
    contraseña = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Contraseña'
    )
    fecha_creacion = forms.DateTimeField(
        required=False,
        label='Fecha de creación',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'input'},
            format='%Y-%m-%dT%H:%M'
        )
    )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s'-]+", nombre):
            raise forms.ValidationError('El nombre de usuario solo puede contener letras, espacios, apóstrofes o guiones.')
        return nombre

    def clean_contraseña(self):
        contraseña = self.cleaned_data.get('contraseña', '').strip()
        if len(contraseña) < 6:
            raise forms.ValidationError('La contraseña debe tener al menos 6 caracteres.')
        if not re.search(r'[A-Za-z]', contraseña) or not re.search(r'\d', contraseña):
            raise forms.ValidationError('La contraseña debe incluir letras y números.')
        return contraseña

    class Meta:
        model = User
        fields = ('nombre', 'contraseña', 'cargo', 'fecha_creacion')

    def save(self, commit=True):
        """Hashea la contraseña antes de guardar"""
        user = super().save(commit=False)
        raw_password = self.cleaned_data.get('contraseña')
        if raw_password:
            user.set_password(raw_password)
        if not user.fecha_creacion:
            user.fecha_creacion = timezone.now()
        if commit:
            user.save()
        return user
