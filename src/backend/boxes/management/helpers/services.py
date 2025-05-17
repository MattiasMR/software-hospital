from datetime import time, datetime
from django.utils import timezone
from ...models import Box, Medico, Consulta

HORAS_FRANJAS = range(8, 22)  # 8:00 a 22:00
OCCUPIED_STATES = {"Completada", "Pendiente", "Confirmada"}

def get_box_franjas(box, fecha):
    """Devuelve la lista de franjas horarias y su estado ('Ocupado', 'Libre', etc.) para ese box y día"""
    consultas = box.consultas.filter(fechaHoraInicio__date=fecha)
    franjas = []

    if box.disponibilidadBox.disponibilidad == "Inhabilitado":
        for h in HORAS_FRANJAS:
            franjas.append({
                "inicio": f"{h:02d}:00",
                "fin": f"{h+1:02d}:00",
                "medico": "—",
                "especialidad": "—",
                "estado": "Inhabilitado",
            })
        return franjas

    for h in HORAS_FRANJAS:
        ini = time(h, 0)
        fin = time(h+1, 0)
        ini_dt = datetime.combine(fecha, ini)
        fin_dt = datetime.combine(fecha, fin)

        # Asegurarse de que las fechas sean aware
        ini_dt = timezone.make_aware(ini_dt, timezone.get_current_timezone())
        fin_dt = timezone.make_aware(fin_dt, timezone.get_current_timezone())

        consulta_encontrada = None
        for c in consultas:
            # Asegúrate de que las consultas también sean aware
            inicio_c = c.fechaHoraInicio if c.fechaHoraInicio.tzinfo else timezone.make_aware(c.fechaHoraInicio)
            fin_c = c.fechaHoraFin if c.fechaHoraFin.tzinfo else timezone.make_aware(c.fechaHoraFin)
            
            # Realiza la comparación ahora con fechas aware
            if inicio_c < fin_dt and fin_c > ini_dt:
                consulta_encontrada = c
                break

        if consulta_encontrada:
            franjas.append({
                "inicio": f"{ini:%H:%M}",
                "fin": f"{fin:%H:%M}",
                "medico": consulta_encontrada.medico.nombreCompleto if consulta_encontrada.medico else "—",
                "especialidad": consulta_encontrada.medico.especialidad.nombreEspecialidad if consulta_encontrada.medico else "—",
                "estado": consulta_encontrada.estadoConsulta.estadoConsulta,
            })
        else:
            franjas.append({
                "inicio": f"{ini:%H:%M}",
                "fin": f"{fin:%H:%M}",
                "medico": "—",
                "especialidad": "—",
                "estado": "Libre",
            })
    return franjas

def calcular_porcentaje_ocupacion(franjas):
    total = len([f for f in franjas if f["estado"] != "Inhabilitado"])
    EXCLUIR = ("Libre", "Inhabilitado", "Cancelada")
    ocupadas = sum(1 for f in franjas if f["estado"] not in EXCLUIR)

    return int((ocupadas / total) * 100) if total else 0

def get_boxes_with_kpis(target_date=None):
    """Lista de todos los boxes con su ocupación y estado en el día seleccionado"""
    if not target_date:
        target_date = timezone.localdate()
    results = []
    for box in Box.objects.select_related("disponibilidadBox", "pasillo").all():
        franjas = get_box_franjas(box, target_date)
        porcentaje_ocupacion = calcular_porcentaje_ocupacion(franjas)
        
        now = timezone.localtime()
        hora_actual = now.hour - 4  # Ajustar la hora a UTC-4
        franja_actual = next(
            (
                f for f in franjas
                if (
                    isinstance(f["inicio"], str) and f["inicio"] != "--" and
                    int(f["inicio"][:2]) <= hora_actual < int(f["fin"][:2])
                )
            ),
            None
        )
        disponibilidad = (
                "Ocupado" if franja_actual["estado"] in OCCUPIED_STATES
                else franja_actual["estado"]          # Libre o Inhabilitado
            )
        medico_asignado = franja_actual["medico"] if franja_actual and franja_actual["medico"] != "—" else None
        results.append({
            "idBox": box.idBox,
            "numeroBox": box.idBox,
            "pasillo": box.pasillo.nombrePasillo,
            "disponibilidad": disponibilidad,
            "medicoAsignado": medico_asignado,
            "porcentajeOcupacion": porcentaje_ocupacion,
        })
    return results
