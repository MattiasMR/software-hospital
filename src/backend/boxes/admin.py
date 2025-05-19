# backend/boxes/admin.py

from django.contrib import admin
from .models import (
    DisponibilidadBox,
    Especialidad,
    Jornada,
    Medico,
    Pasillo,
    Box,
    BoxEspecialidad,
    EstadoConsulta,
    Consulta,
)

@admin.register(DisponibilidadBox)
class DisponibilidadBoxAdmin(admin.ModelAdmin):
    list_display = ('id', 'disponibilidad')
    search_fields = ('disponibilidad',)

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombreEspecialidad')
    search_fields = ('nombreEspecialidad',)

@admin.register(Jornada)
class JornadaAdmin(admin.ModelAdmin):
    list_display = ('id', 'jornadaInicio', 'jornadaFin')
    list_filter = ('jornadaInicio', 'jornadaFin')

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombreCompleto', 'especialidad', 'jornada')
    search_fields = ('nombreCompleto',)
    list_filter = ('especialidad', 'jornada')

@admin.register(Pasillo)
class PasilloAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombrePasillo')
    search_fields = ('nombrePasillo',)

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('id', 'pasillo', 'disponibilidadBox')
    list_filter = ('pasillo', 'disponibilidadBox')

@admin.register(BoxEspecialidad)
class BoxEspecialidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'box', 'especialidad')
    list_filter = ('box', 'especialidad')

@admin.register(EstadoConsulta)
class EstadoConsultaAdmin(admin.ModelAdmin):
    list_display = ('id', 'estadoConsulta')
    search_fields = ('estadoConsulta',)

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'box',
        'medico',
        'estadoConsulta',
        'fechaHoraInicio',
        'fechaHoraFin',
    )
    list_filter = ('estadoConsulta', 'box', 'medico')
    search_fields = (
        'box__id',
        'medico__nombreCompleto',
    )
    date_hierarchy = 'fechaHoraInicio'
