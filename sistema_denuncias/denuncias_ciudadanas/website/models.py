from django.db import models
from django.forms import ModelForm, TextInput, Textarea


# Create your models here.
class Post(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "contenido"]
        widgets = {
            "titulo": TextInput(attrs={"class": "form-control"}),
            "contenido": Textarea(attrs={"class": "form-control"}),
        }


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Report(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField()
  location = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class ReportImage(models.Model):
    report = models.ForeignKey(Report, on_delete=models.PROTECT)
    image_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=255)

class ReportCategory(models.Model):
    report = models.ForeignKey(Report, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

class ReportComment(models.Model):
    report = models.ForeignKey(Report, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Geolocation(models.Model):
    report = models.ForeignKey(Report, on_delete=models.PROTECT)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

categorias = [
    [0, "Lugar de explotación"],
    [1, "Uso y/o contaminación de recursos naturales"],
    [2, "Residuos, emisiones e inmisiones"]
]
class RegistroDenuncia(models.Model):
    titulo = models.CharField(max_length=20, verbose_name= 'Ingrese titulo de denuncia')
    causa = models.IntegerField(choices=categorias, verbose_name='Causa de conflicto')
    asunto = models.TextField(max_length=200, verbose_name='Ingrese asunto')
    imagen = models.ImageField(upload_to='imagenes/', default='default.jpg')
    fecha_envio = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de ingreso')
    consentimiento = models.BooleanField(default=False, verbose_name='Acepto terminos y condiciones')
    # localizacion_geo = [variable del post]
    # usuario denunciante = [variable del post]

    
    def __str__(self) -> str:
        return self.titulo