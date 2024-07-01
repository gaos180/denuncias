from django.db import models
from django.forms import ModelForm, TextInput, Textarea
import datetime

from django.contrib.auth.models import User



categorias = [
    [0, "Lugar de explotación"],
    [1, "Uso y/o contaminación de recursos naturales"],
    [2, "Residuos, emisiones e inmisiones"]
]

estados = [
    [0, "En revisión"],
    [1, "En procedimiento"],
    [2, "Finalizada"],
    [3, "Rechazada"],
    [4, "Deshabilitada"]

]
class Denuncia(models.Model):
    titulo = models.CharField(max_length=60, verbose_name= 'Ingrese titulo de denuncia')
    causa = models.IntegerField(choices=categorias, verbose_name='Causa de conflicto')
    asunto = models.TextField(max_length=200, verbose_name='Ingrese asunto')
    fecha_suceso = models.DateField(null=True, blank=True)
    hora_suceso = models.TimeField(null=True, blank=True)
    imagen = models.ImageField(upload_to='imagenes/', default='default.jpg')
    fecha_envio = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de ingreso')
    consentimiento = models.BooleanField(default=False)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    username = models.ForeignKey(User, on_delete=models.PROTECT, default=1)
    estado = models.IntegerField(choices=estados, verbose_name='Estado de la denuncia', default=0)


    def __str__(self) -> str:
        return self.titulo