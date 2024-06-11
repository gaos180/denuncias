from django import forms
from .models import Report, RegistroDenuncia
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class RegistroDenuncia(forms.ModelForm):
    class Meta:
        model = RegistroDenuncia
        fields = ['titulo', 'causa', 'asunto', 'imagen', 'consentimiento']