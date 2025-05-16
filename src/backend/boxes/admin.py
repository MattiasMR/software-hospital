from django.contrib import admin
from .models import (
    DisponibilidadBox,
    TipoBox,
    Especialidad,
    Jornada,
    EstadoConsulta,
    Box,
    Medico,
    Consulta,
)

@admin.register(DisponibilidadBox)
class DisponibilidadBoxAdmin(admin.ModelAdmin):
    list_display = ('idDisponibilidadBox', 'disponibilidad')

@admin.register(TipoBox)
class TipoBoxAdmin(admin.ModelAdmin):
    list_display = ('idTipoBox', 'tipoBox')

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('idEspecialidad', 'nombreEspecialidad')

@admin.register(Jornada)
class JornadaAdmin(admin.ModelAdmin):
    list_display = ('idJornada', 'jornadaInicio', 'jornadaFin')

@admin.register(EstadoConsulta)
class EstadoConsultaAdmin(admin.ModelAdmin):
    list_display = ('idEstadoConsulta', 'estadoConsulta')

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('idBox', 'numeroBox', 'tipoBox', 'disponibilidadBox')
    list_filter  = ('tipoBox', 'disponibilidadBox')

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('idMedico', 'nombreCompleto', 'especialidad', 'jornada')
    list_filter  = ('especialidad',)

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = (
        'idConsulta',
        'box',
        'medico',
        'estadoConsulta',
        'fechaHoraInicio',
        'fechaHoraFin'
    )
    list_filter = ('estadoConsulta', 'box')
