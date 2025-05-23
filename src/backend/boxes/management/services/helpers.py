# boxes/helpers.py
from datetime import time, datetime
from collections import defaultdict
from django.utils import timezone
from django.db.models import Prefetch

from ...models import (
    Box,
    Consulta,
    EstadoConsulta,
    DisponibilidadBox,
)

HORAS_FRANJAS = range(4, 22)  # 08:00 – 22:00

def _estado_consulta_display(consulta, ini_dt, fin_dt):
    estado = consulta.estadoConsulta.estadoConsulta
    now = timezone.localtime()

    if estado == EstadoConsulta.Estado.CANCELADA:
        return "Cancelada"
    if estado == EstadoConsulta.Estado.PENDIENTE:
        return "Pendiente"
    # Confirmada – subestados según la hora
    if ini_dt <= now < fin_dt:
        return "En curso"
    elif now >= fin_dt:
        return "Terminada"
    else:
        return "Confirmada"

def get_box_franjas(box, fecha):
    tz = timezone.get_current_timezone()
    inicio_dia = timezone.make_aware(datetime.combine(fecha, time.min), tz)
    fin_dia = timezone.make_aware(datetime.combine(fecha, time.max), tz)
    consultas = (
        box.consultas
           .filter(
               fechaHoraInicio__gte=inicio_dia,
               fechaHoraInicio__lt=fin_dia
           )
           .select_related("medico__especialidad", "estadoConsulta")
    )

    franjas = []

    # Inhabilitado todo el día
    if box.disponibilidadBox.disponibilidad == DisponibilidadBox.Estado.INHABILITADO:
        for h in HORAS_FRANJAS:
            franjas.append({
                "inicio": f"{h:02d}:00",
                "fin":    f"{h+1:02d}:00",
                "medico": None,
                "especialidad": None,
                "estado": "Inhabilitado",
            })
        return franjas

    for h in HORAS_FRANJAS:
        ini_naive = datetime.combine(fecha, time(h, 0))
        fin_naive = datetime.combine(fecha, time(h+1, 0))
        ini_dt = timezone.make_aware(ini_naive, tz)
        fin_dt = timezone.make_aware(fin_naive, tz)

        consulta = next(
            (
                c for c in consultas
                if c.fechaHoraInicio < fin_dt and c.fechaHoraFin > ini_dt
            ),
            None,
        )

        if consulta:
            estado = _estado_consulta_display(consulta, ini_dt, fin_dt)
            franjas.append({
                "inicio": ini_dt.strftime("%H:%M"),
                "fin":    fin_dt.strftime("%H:%M"),
                "medico": consulta.medico.nombreCompleto if consulta.medico else None,
                "especialidad": (
                    consulta.medico.especialidad.nombreEspecialidad
                    if consulta.medico else None
                ),
                "estado": estado,
            })
        else:
            franjas.append({
                "inicio": ini_dt.strftime("%H:%M"),
                "fin":    fin_dt.strftime("%H:%M"),
                "medico": None,
                "especialidad": None,
                "estado": "Libre",
            })

    return franjas

def calcular_porcentaje_ocupacion(franjas):
    utilis = [f for f in franjas if f["estado"] != "Inhabilitado"]
    if not utilis:
        return 0
    ocup = sum(1 for f in utilis if f["estado"] != "Libre")
    return int((ocup / len(utilis)) * 100)

def get_boxes_with_kpis(target_date=None):
    if target_date is None:
        target_date = timezone.localdate()

    boxes = (
        Box.objects
           .select_related("pasillo", "disponibilidadBox")
           .prefetch_related(
               Prefetch(
                   "consultas",
                   queryset=Consulta.objects.select_related("medico__especialidad", "estadoConsulta")
               ),
               "especialidades"
           )
    )

    now = timezone.localtime()

    results = []
    for box in boxes:
        franjas = get_box_franjas(box, target_date)
        porcentaje = calcular_porcentaje_ocupacion(franjas)

        medicos_del_dia = sorted({
            f["medico"] for f in franjas if f["medico"] is not None
        })

        especialidades_box = [esp.nombreEspecialidad for esp in box.especialidades.all()]

        # Estado actual del box
        if box.disponibilidadBox.disponibilidad == DisponibilidadBox.Estado.INHABILITADO:
            disponibilidad = "Inhabilitado"
            medico_actual  = None
        else:
            consultas_ahora = box.consultas.filter(
                fechaHoraInicio__lte=now,
                fechaHoraFin__gt=now,
            )
            if consultas_ahora.exists():
                disponibilidad = "Ocupado"
                medico = consultas_ahora.first().medico
                medico_actual = medico.nombreCompleto if medico else None
            else:
                disponibilidad = "Libre"
                medico_actual  = None

        results.append({
            "idBox": box.id,
            "disponibilidad": disponibilidad,
            "pasillo": box.pasillo.nombrePasillo,
            "medicoAsignado": medico_actual,
            "porcentajeOcupacion": porcentaje,
            "medicosDelDia": medicos_del_dia,
            "especialidades": especialidades_box,
        })

    return results

def get_box_turnos(box, fecha):
    """
    Para un box y un día, devuelve para cada médico:
    - su rango de jornada (desde Medico.jornada)
    - cuántas horas de esa jornada realmente estuvo en consultas
    - % de ocupación (horas trabajadas / total jornada)
    - la lista de consultas (inicio, fin, estado)
    """
    tz = timezone.get_current_timezone()
    inicio_dia = timezone.make_aware(datetime.combine(fecha, time.min), tz)
    fin_dia    = timezone.make_aware(datetime.combine(fecha, time.max), tz)

    consultas = (
        box.consultas
           .filter(fechaHoraInicio__gte=inicio_dia, fechaHoraInicio__lt=fin_dia)
           .select_related("medico__especialidad", "medico__jornada", "estadoConsulta")
    )

    grupos = defaultdict(list)
    for c in consultas:
        grupos[c.medico].append(c)

    turnos = []
    for medico, cons in grupos.items():
        jornada = medico.jornada
        j_ini = timezone.make_aware(datetime.combine(fecha, jornada.jornadaInicio), tz)
        j_fin = timezone.make_aware(datetime.combine(fecha, jornada.jornadaFin), tz)
        jornada_secs = (j_fin - j_ini).total_seconds()

        ocup_secs = 0
        consultas_data = []
        for c in cons:
            start = max(c.fechaHoraInicio, j_ini)
            end   = min(c.fechaHoraFin,    j_fin)
            if end > start:
                ocup_secs += (end - start).total_seconds()
            consultas_data.append({
                "inicio": start.strftime("%H:%M"),
                "fin":    end.strftime("%H:%M"),
                "estado": c.estadoConsulta.estadoConsulta,
            })

        porcentaje = int((ocup_secs / jornada_secs) * 100) if jornada_secs else 0
        turnos.append({
            "medico": medico.nombreCompleto,
            "especialidad": medico.especialidad.nombreEspecialidad,
            "rango": f"{jornada.jornadaInicio.strftime('%H:%M')}-{jornada.jornadaFin.strftime('%H:%M')}",
            "horasOcupadas": round(ocup_secs/3600, 2),
            "porcentajeOcupacion": porcentaje,
            "consultas": consultas_data,
        })

    return turnos
