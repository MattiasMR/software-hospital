from django.contrib import admin
from .models import (
    Box,
    DisponibilidadBox,
    Pasillo,
    Especialidad,
    Jornada,
    EstadoConsulta,
    Medico,
    Consulta,
)

@admin.register(DisponibilidadBox)
class DisponibilidadBoxAdmin(admin.ModelAdmin):
    list_display  = ("idDisponibilidadBox", "disponibilidad")
    search_fields = ("disponibilidad",)

@admin.register(Pasillo)
class PasilloAdmin(admin.ModelAdmin):
    list_display  = ("idPasillo", "nombrePasillo")
    search_fields = ("nombrePasillo",)

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display  = ("idEspecialidad", "nombreEspecialidad")
    search_fields = ("nombreEspecialidad",)

@admin.register(Jornada)
class JornadaAdmin(admin.ModelAdmin):
    list_display  = ("idJornada", "jornadaInicio", "jornadaFin")
    list_filter   = ("jornadaInicio", "jornadaFin")

@admin.register(EstadoConsulta)
class EstadoConsultaAdmin(admin.ModelAdmin):
    list_display  = ("idEstadoConsulta", "estadoConsulta")
    search_fields = ("estadoConsulta",)

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display  = ("idMedico", "nombreCompleto", "especialidad", "jornada")
    list_filter   = ("especialidad",)
    search_fields = ("nombreCompleto",)

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display  = ("idBox", "pasillo", "disponibilidadBox")
    list_filter   = ("pasillo", "disponibilidadBox")
    search_fields = ("idBox",)

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display  = (
        "idConsulta",
        "box",
        "medico",
        "estadoConsulta",
        "fechaHoraInicio",
        "fechaHoraFin",
    )
    list_filter   = ("estadoConsulta", "fechaHoraInicio", "box")
    search_fields = ("box__idBox", "medico__nombreCompleto")
