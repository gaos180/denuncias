from django import forms
from .models import Report, RegistroDenuncia
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'description', 'location']
        labels = {
            'title': 'Título de Denuncia',
            'description': 'Descripción de la Denuncia',
            'location': 'Localidad',
        }

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido")
    email = forms.EmailField(required=True, label="Correo Electrónico")  # Add explicit email validation

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']

        # Check for existing usernames (consider case-insensitive check if needed)
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("El nombre de usuario ya existe. Por favor, elija otro nombre.")
        return username
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise ValidationError('Las contraseñas no coinciden.')
        return cd['password2']



class RegistroDeDenuncia(forms.ModelForm):
    class Meta:
        model = RegistroDenuncia
        fields = ['titulo', 'causa', 'asunto', 'fecha_suceso', 'hora_suceso', 'imagen', 'consentimiento']
        widgets = {
            'fecha_suceso': forms.DateInput(attrs={'type': 'date'}),
            'hora_suceso': forms.TimeInput(attrs={'type': 'time'}),
        }
