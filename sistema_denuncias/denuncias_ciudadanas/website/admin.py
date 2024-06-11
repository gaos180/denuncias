from django.contrib import admin
from .models import Post, RegistroDenuncia

# Register your models here.
admin.site.register(Post)

class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'causa', 'asunto', 'imagen', 'latitude','longitude','fecha_envio')
    search_fields = ('titulo', 'causa', 'asunto', 'fecha_envio')
    list_filter = ('titulo', 'causa', 'asunto', 'fecha_envio')

admin.site.register(RegistroDenuncia, ConsultaAdmin)