
"""
from django import forms
from .models import Report
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        #fields = ['user', 'title', 'description', 'status', 'location']
        fields = ['title', 'description', 'location']
"""

from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'description', 'location']
        labels = {
            'title': 'Título de Denuncia',
            'description': 'Descripción de la Denuncia',
            'location': 'Localidad',
        }
