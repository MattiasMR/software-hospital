from ...models import Box, Consulta, Especialidad
from django.utils import timezone

from datetime import datetime, timedelta
from collections import defaultdict

def get_boxes_with_kpis(target_date=None):
    """
    Devuelve una lista de diccionarios con el estado de cada box,
    el médico asignado en la hora actual, y el porcentaje de ocupación diaria.
    """
    if target_date is None:
        now = timezone.localtime()
        target_date = now.date()
    else:
        now = timezone.localtime()
    
    boxes = (
        Box.objects
        .select_related('tipoBox', 'disponibilidadBox', 'pasillo')
        .prefetch_related('consultas__medico', 'consultas__estadoConsulta')
        .all()
    )

    results = []
    for box in boxes:
        consultas = box.consultas.filter(
            fechaHoraInicio__date=target_date
        )
        total_consultas = consultas.count()
        ocupadas = consultas.filter(estadoConsulta__estadoConsulta='Ocupado').count()
        porcentaje_ocupacion = int((ocupadas / total_consultas) * 100) if total_consultas else 0

        
        consulta_actual = consultas.filter(
            fechaHoraInicio__lte=now,
            fechaHoraFin__gte=now,
            estadoConsulta__estadoConsulta='Ocupado'
        ).select_related('medico').first()
        medico_asignado = consulta_actual.medico.nombreCompleto if consulta_actual else None

        # Puedes agregar más KPIs aquí si los necesitas

        results.append({
            "idBox": box.idBox,
            "numeroBox": getattr(box, "numeroBox", box.idBox),
            "tipoBox": box.tipoBox.tipoBox,
            "disponibilidad": box.disponibilidadBox.disponibilidad,
            "pasillo": box.pasillo.nombrePasillo,
            "medicoAsignado": medico_asignado,
            "porcentajeOcupacion": porcentaje_ocupacion,
        })
    return results

def get_reportes_kpis(date_from=None, date_to=None, especialidad=None):
    """
    Calcula KPIs para los boxes en el rango de fechas dado.
    Devuelve: % ocupación global, tiempos muertos por box, uso por especialidad.
    """
    
    # Parse fechas o usa el día actual por defecto
    today = timezone.localdate()
    if not date_from:
        date_from = today
    if not date_to:
        date_to = today

    consultas = Consulta.objects.filter(
        fechaHoraInicio__date__gte=date_from,
        fechaHoraInicio__date__lte=date_to
    )
    if especialidad:
        consultas = consultas.filter(medico__especialidad__nombreEspecialidad=especialidad)

    total_consultas = consultas.count()
    ocupadas = consultas.filter(estadoConsulta__estadoConsulta='Ocupado').count()
    porcentaje_ocupacion = round((ocupadas / total_consultas) * 100, 2) if total_consultas else 0

    # Tiempos muertos por box
    tiempos_muertos = defaultdict(int)
    for box in Box.objects.all():
        consultas_box = consultas.filter(box=box).order_by('fechaHoraInicio')
        last_end = None
        for consulta in consultas_box:
            if last_end:
                delta = (consulta.fechaHoraInicio - last_end).total_seconds() // 60  # minutos
                if delta > 0:
                    tiempos_muertos[box.idBox] += delta
            last_end = consulta.fechaHoraFin
    tiempos_muertos = dict(tiempos_muertos)

    # Uso por especialidad
    uso_por_especialidad = defaultdict(int)
    for consulta in consultas:
        esp = consulta.medico.especialidad.nombreEspecialidad
        uso_por_especialidad[esp] += 1

    return {
        "porcentaje_ocupacion": porcentaje_ocupacion,
        "tiempos_muertos": tiempos_muertos,
        "uso_por_especialidad": uso_por_especialidad,
        "rango": {"desde": str(date_from), "hasta": str(date_to)},
    }