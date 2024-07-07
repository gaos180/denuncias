from django import forms
from .models import Denuncia
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido")
    email = forms.EmailField(required=True, label="Correo Electrónico")  # Add explicit email validation

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("El nombre de usuario ya existe. Por favor, elija otro nombre.")
        return username
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise ValidationError('Las contraseñas no coinciden.')
        return cd['password2']

class RegistroDeDenuncia(forms.ModelForm):

    consentimiento = forms.BooleanField(
        required=True,
        label=mark_safe('Acepto los <a href="/terminos-y-condiciones/" target="_blank">términos y condiciones</a>')
    )
    
    class Meta:
        model = Denuncia
        fields = ['titulo', 'causa', 'asunto', 'fecha_suceso', 'hora_suceso', 'imagen', 'consentimiento']
        widgets = {
            'fecha_suceso': forms.DateInput(attrs={'type': 'date'}),
            'hora_suceso': forms.TimeInput(attrs={'type': 'time'}),
        }

class RegistroDeUsuario(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_staff']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Email',
            'is_staff': 'Staff',
        }
