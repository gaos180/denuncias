from django.contrib import admin
from .models import Denuncia


class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'causa', 'asunto', 'fecha_suceso','hora_suceso','imagen','latitude','longitude','fecha_envio')
    search_fields = ('titulo', 'causa', 'asunto', 'fecha_suceso','hora_suceso','fecha_envio')
    list_filter = ('titulo', 'causa', 'asunto', 'fecha_suceso','hora_suceso','fecha_envio')

admin.site.register(Denuncia, ConsultaAdmin)