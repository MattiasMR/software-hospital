# boxes/admin.py

from django.contrib import admin
from .models import (
    DisponibilidadBox,
    TipoBox,
    Pasillo,
    Especialidad,
    Jornada,
    EstadoConsulta,
    Box,
    Medico,
    Consulta,
)


@admin.register(DisponibilidadBox)
class DisponibilidadBoxAdmin(admin.ModelAdmin):
    list_display  = ("pk", "disponibilidad")
    search_fields = ("disponibilidad",)


@admin.register(TipoBox)
class TipoBoxAdmin(admin.ModelAdmin):
    list_display  = ("pk", "tipoBox")
    search_fields = ("tipoBox",)


@admin.register(Pasillo)
class PasilloAdmin(admin.ModelAdmin):
    list_display  = ("pk", "nombrePasillo")
    search_fields = ("nombrePasillo",)


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display  = ("pk", "nombreEspecialidad")
    search_fields = ("nombreEspecialidad",)


@admin.register(Jornada)
class JornadaAdmin(admin.ModelAdmin):
    list_display  = ("pk", "jornadaInicio", "jornadaFin")
    list_filter   = ("jornadaInicio", "jornadaFin")


@admin.register(EstadoConsulta)
class EstadoConsultaAdmin(admin.ModelAdmin):
    list_display  = ("pk", "estadoConsulta")
    search_fields = ("estadoConsulta",)


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display  = ("pk", "tipoBox", "disponibilidadBox", "pasillo", "medico")
    list_filter   = ("tipoBox", "disponibilidadBox", "pasillo", "medico")
    search_fields = ("idBox",)


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display  = ("pk", "nombreCompleto", "especialidad", "jornada")
    list_filter   = ("especialidad",)
    search_fields = ("nombreCompleto",)


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display  = (
        "pk",
        "box",
        "medico",
        "estadoConsulta",
        "fechaHoraInicio",
        "fechaHoraFin",
    )
    list_filter   = ("estadoConsulta", "fechaHoraInicio")
    search_fields = ("box__numeroBox", "medico__nombreCompleto")
