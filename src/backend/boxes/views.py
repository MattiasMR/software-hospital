from collections import defaultdict
import json, time
from datetime import datetime, timedelta, time
from typing import Callable, Iterator, List
from rest_framework.generics import ListAPIView

from django.http import StreamingHttpResponse
from django.utils import timezone
from django.utils.dateparse import parse_date
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Consulta, Medico, Especialidad, Box
from .serializers import BoxDetalleSerializer, BoxStatusSimpleSerializer
from .management.services.helpers import (  
    get_box_franjas, # capaz haya que sacarlo
    get_box_turnos,
    get_boxes_with_kpis,
)

REFRESH_SECONDS = 2  # poll interno SSE

def _sse_stream(generator_fn: Callable[[], Iterator[dict]]) -> StreamingHttpResponse:
    def event_stream() -> Iterator[str]:
        yield "retry: 4000\n\n"  # 4 s entre reconexiones automáticas en el cliente
        for payload in generator_fn():
            yield f"data: {json.dumps(payload)}\n\n"

    response = StreamingHttpResponse(
        streaming_content=event_stream(),
        content_type="text/event-stream",
    )
    response["Cache-Control"] = "no-cache"
    return response

def _boxes_generator(target_date) -> Iterator[List[dict]]:
    while True:
        yield get_boxes_with_kpis(target_date)
        time.sleep(REFRESH_SECONDS)

def boxes_stream(request):
    date_str = request.GET.get("date")
    target_date = (
        datetime.strptime(date_str, "%Y-%m-%d").date()
        if date_str else timezone.localdate()
    )
    return _sse_stream(lambda: _boxes_generator(target_date))

class BoxDetalleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, idBox: int):
        date_str = request.GET.get("date")
        fecha = (
            datetime.strptime(date_str, "%Y-%m-%d").date()
            if date_str else timezone.localdate()
        )

        try:
            box = Box.objects.select_related("disponibilidadBox", "pasillo").get(id=idBox)
        except Box.DoesNotExist:
            return Response({"detail": "Box no encontrado."}, status=404)

        turnos = get_box_turnos(box, fecha)
        payload = {
            "pasillo": box.pasillo.nombrePasillo,
            "turnos":  turnos,
        }
        serializer = BoxDetalleSerializer(payload)
        return Response(serializer.data)

class BoxFranjasView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, idBox):
        date_str = request.GET.get("date")
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else timezone.localdate()
        try:
            box = Box.objects.get(id=idBox)
        except Box.DoesNotExist:
            return Response({"detail": "Box no encontrado."}, status=404)
        franjas = get_box_franjas(box, target_date)
        return Response(franjas)


class BoxStatusListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BoxStatusSimpleSerializer

    def get_queryset(self):
        target_date = self.request.GET.get("date")
        if target_date:
            target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        else:
            target_date = timezone.localdate()
        boxes_data = get_boxes_with_kpis(target_date)

        # Filtros: especialidad, pasillo, médico
        espec = self.request.GET.get("especialidad")
        pasillo = self.request.GET.get("pasillo")
        medico = self.request.GET.get("medico")
        if espec:
            boxes_data = [b for b in boxes_data if espec in b.get("especialidades", [])]
        if pasillo:
            boxes_data = [b for b in boxes_data if b["pasillo"] == pasillo]
        if medico:
            boxes_data = [b for b in boxes_data if medico in b.get("medicosDelDia", [])]
        return boxes_data

    def get(self, request, *args, **kwargs):
        # DRF ListAPIView get_queryset expects a queryset, but here we use a list
        data = self.get_queryset()
        return Response(self.serializer_class(data, many=True).data)
    
class ReportesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dfrom = request.query_params.get("date_from")
        dto   = request.query_params.get("date_to")
        if not (dfrom and dto):
            return Response({"detail": "Faltan date_from o date_to"}, status=400)

        start = parse_date(dfrom)
        end   = parse_date(dto)
        if not (start and end):
            return Response({"detail": "Formato de fecha inválido"}, status=400)
        if start > end:
            return Response({"detail": "date_from debe ser ≤ date_to"}, status=400)

        total_days = 0
        sum_ocup   = 0.0

        medicos_por_franja     = defaultdict(int)
        uso_por_especialidad   = defaultdict(int)
        doctor_hours           = defaultdict(int)
        box_hours              = defaultdict(int)

        day = start
        while day <= end:
            snapshot = get_boxes_with_kpis(day)
            if snapshot:
                total_days += 1
                sum_ocup += sum(b["porcentajeOcupacion"] for b in snapshot) / len(snapshot)

            for box in Box.objects.all():
                franjas = get_box_franjas(box, day)
                for f in franjas:
                    estado = f["estado"]
                    if estado in ("Libre", "Inhabilitado", "Cancelada"):
                        continue

                    slot = f"{f['inicio']}-{f['fin']}"
                    medicos_por_franja[slot] += 1

                    spec = f["especialidad"] or "—"
                    uso_por_especialidad[spec] += 1

                    doc = f["medico"]
                    if doc:
                        doctor_hours[doc] += 1

                    box_hours[box.id] += 1

            day += timedelta(days=1)

        porcentaje_ocupacion = round(sum_ocup / total_days, 2) if total_days else 0

        if doctor_hours:
            name, hrs = max(doctor_hours.items(), key=lambda x: x[1])
        else:
            name, hrs = "—", 0
        medico_lider = {"name": name, "horas": hrs}

        if box_hours:
            bid, bhrs = max(box_hours.items(), key=lambda x: x[1])
        else:
            bid, bhrs = None, 0
        box_mayor_uso = {"id": bid, "horas": bhrs}

        if uso_por_especialidad:
            spec_name, spec_hrs = max(uso_por_especialidad.items(), key=lambda x: x[1])
        else:
            spec_name, spec_hrs = "—", 0
        especialidad_mas_demanda = {"name": spec_name, "horas": spec_hrs}

        ranking = sorted(box_hours.items(), key=lambda x: x[1], reverse=True)[:5]
        ranking_boxes = [{"id": bid, "horas": hrs} for bid, hrs in ranking]

        ranking = sorted(doctor_hours.items(), key=lambda x: x[1], reverse=True)[:5]
        ranking_medicos = [{"id": bid, "horas": hrs} for bid, hrs in ranking]

        return Response({
            "porcentaje_ocupacion": porcentaje_ocupacion,
            "medicos_por_franja": dict(medicos_por_franja),
            "uso_por_especialidad": dict(uso_por_especialidad),
            "medico_lider": medico_lider,
            "box_mayor_uso": box_mayor_uso,
            "especialidad_mas_demanda": especialidad_mas_demanda,
            "ranking_boxes": ranking_boxes,
            "ranking_medicos": ranking_medicos,
        })

class BuscarMedicosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tz = timezone.get_current_timezone()
        today = timezone.localdate()

        inicio = timezone.make_aware(datetime.combine(today, time.min), tz)
        fin = timezone.make_aware(datetime.combine(today, time.max), tz)

        consultas_hoy = Consulta.objects.filter(fechaHoraInicio__gte=inicio, fechaHoraInicio__lte=fin)
        cantidad_consultas = consultas_hoy.count()

        doctores_ids = consultas_hoy.values_list("medico", flat=True).distinct()
        doctores = (
            Medico.objects.filter(id__in=doctores_ids)
            .select_related("especialidad")
            .values("id", "nombreCompleto", "especialidad__nombreEspecialidad")
        )
        doctores_list = list(doctores)

        return Response({
            "doctores_hoy": doctores_list,
        }) 

class ResumenDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tz = timezone.get_current_timezone()
        today = timezone.localdate()

        inicio = timezone.make_aware(datetime.combine(today, time.min), tz)
        fin = timezone.make_aware(datetime.combine(today, time.max), tz)

        consultas_hoy = Consulta.objects.filter(fechaHoraInicio__gte=inicio, fechaHoraInicio__lte=fin)
        cantidad_consultas = consultas_hoy.count()

        doctores_ids = consultas_hoy.values_list("medico", flat=True).distinct()
        doctores = (
            Medico.objects.filter(id__in=doctores_ids)
            .select_related("especialidad")
            .values("id", "nombreCompleto", "especialidad__nombreEspecialidad")
        )
        doctores_list = list(doctores)

        especialidades_qs = (
            doctores.values("especialidad__nombreEspecialidad")
            .annotate(cantidad_medicos=models.Count("id"))
            .order_by("-cantidad_medicos")
        )
        especialidades_disponibles = [
            {
                "especialidad": e["especialidad__nombreEspecialidad"],
                "cantidad_medicos": e["cantidad_medicos"]
            }
            for e in especialidades_qs
        ]

        top_especialidades_qs = (
            consultas_hoy.values("medico__especialidad__nombreEspecialidad")
            .annotate(cantidad=models.Count("id"))
            .order_by("-cantidad")[:]
        )
        top_3_especialidades = [
            {
                "especialidad": e["medico__especialidad__nombreEspecialidad"],
                "consultas": e["cantidad"]
            }
            for e in top_especialidades_qs
        ]

        return Response({
            "consultas_hoy": cantidad_consultas,
            "doctores_hoy": doctores_list,
            "especialidades_disponibles": especialidades_disponibles,
            "top_especialidades": top_3_especialidades
        })

class BoxDetalleV2View(APIView):
    def get(self, request, idBox):
        date_str = request.GET.get("date")
        if date_str:
            year, month, day = map(int, date_str.split("-"))
            target_date = datetime(year, month, day).date()
        else:
            target_date = timezone.localdate()

        try:
            box = Box.objects.get(id=idBox)
        except Box.DoesNotExist:
            return Response({"detail": "Box no encontrado."}, status=404)

        tz = timezone.get_current_timezone()
        inicio_dia = timezone.make_aware(datetime.combine(target_date, time(8, 0)), tz)
        fin_dia = timezone.make_aware(datetime.combine(target_date, time(20, 0)), tz)

        consultas = Consulta.objects.filter(
            box=box,
            fechaHoraInicio__gte=inicio_dia,
            fechaHoraInicio__lt=fin_dia,
        ).select_related("medico__especialidad", "estadoConsulta").order_by("fechaHoraInicio")

        consultas_list = [
            {
                "medico": c.medico.nombreCompleto,
                "especialidad": c.medico.especialidad.nombreEspecialidad,
                "inicio": c.fechaHoraInicio.astimezone(tz).strftime("%H:%M"),
                "fin": c.fechaHoraFin.astimezone(tz).strftime("%H:%M"),
                "estado": c.estadoConsulta.estadoConsulta,
                "minutos": int((c.fechaHoraFin - c.fechaHoraInicio).total_seconds() // 60)
            }
            for c in consultas
        ]

        franjas = []
        for h in range(8, 20, 2):
            ini_franja = timezone.make_aware(datetime.combine(target_date, time(h, 0)), tz)
            fin_franja = timezone.make_aware(datetime.combine(target_date, time(h+2, 0)), tz)
            medicos = set()
            for c in consultas:
                if c.fechaHoraInicio < fin_franja and c.fechaHoraFin > ini_franja:
                    medicos.add((
                        c.medico.nombreCompleto,
                        c.medico.especialidad.nombreEspecialidad
                    ))
            franjas.append({
                "inicio": ini_franja.strftime("%H:%M"),
                "fin": fin_franja.strftime("%H:%M"),
                "medicos": [
                    {"nombre": nombre, "especialidad": esp}
                    for (nombre, esp) in medicos
                ],
            })

        total_min_asignado = 0
        for f in franjas:
            total_min_asignado += len(f["medicos"]) * 120  # 2h = 120min

        total_min_ocupado = sum(c["minutos"] for c in consultas_list)

        return Response({
            "pasillo": box.pasillo.nombrePasillo,
            "franjas": franjas,
            "consultas": consultas_list,
            "total_min_asignado": total_min_asignado,
            "total_min_ocupado": total_min_ocupado,
            "porcentaje_ocupacion": (
                round(100 * total_min_ocupado / total_min_asignado) if total_min_asignado > 0 else 0
            ),
        })

# --- Detalle de KPIs SOLO para un médico ---
class DetalleMedico(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, idMedicos):
        dfrom = request.query_params.get("date_from")
        dto   = request.query_params.get("date_to")
        if not (dfrom and dto):
            return Response({"detail": "Faltan date_from o date_to"}, status=400)

        start = parse_date(dfrom)
        end   = parse_date(dto)
        if not (start and end):
            return Response({"detail": "Formato de fecha inválido"}, status=400)
        if start > end:
            return Response({"detail": "date_from debe ser ≤ date_to"}, status=400)

        try:
            medico_obj = Medico.objects.get(id=idMedicos)
        except Medico.DoesNotExist:
            return Response({"detail": "Médico no encontrado"}, status=404)

        # --- Cálculo de horas trabajadas y posibles ---
        consultas = Consulta.objects.filter(
            medico=medico_obj,
            fechaHoraInicio__date__gte=start,
            fechaHoraInicio__date__lte=end
        ).select_related("box", "medico__especialidad", "estadoConsulta")

        box_hours = defaultdict(float)
        uso_por_especialidad = defaultdict(int)
        horas_por_semana = defaultdict(float)
        consultas_realizadas = 0
        horas_trabajadas = 0.0

        def get_week_str(date):
            y, w, _ = date.isocalendar()
            return f"{y}-W{w:02d}"

        for c in consultas:
            minutos = (c.fechaHoraFin - c.fechaHoraInicio).total_seconds() / 60
            horas = minutos / 60
            box_hours[c.box.id] += horas
            uso_por_especialidad[
                getattr(c.medico.especialidad, "nombreEspecialidad", "Sin especialidad")
            ] += 1
            consultas_realizadas += 1
            horas_trabajadas += horas

            week_str = get_week_str(c.fechaHoraInicio.date())
            horas_por_semana[week_str] += horas

        # Calcular horas posibles según jornada
        total_dias = (end - start).days + 1
        jornada = medico_obj.jornada
        jornada_inicio = jornada.jornadaInicio
        jornada_fin = jornada.jornadaFin
        horas_jornada = (datetime.combine(datetime.min, jornada_fin) - datetime.combine(datetime.min, jornada_inicio)).seconds / 3600
        horas_posibles = horas_jornada * total_dias

        porcentaje_ocupacion = round(100 * horas_trabajadas / horas_posibles, 2) if horas_posibles > 0 else 0

        if box_hours:
            bid, bhrs = max(box_hours.items(), key=lambda x: x[1])
        else:
            bid, bhrs = None, 0
        box_mas_usado = {"id": bid, "horas": round(bhrs, 2)}

        horas_por_semana_list = [
            {"semana": semana, "horas": round(horas, 2)}
            for semana, horas in sorted(horas_por_semana.items())
        ]
        uso_especialidad_dict = dict(uso_por_especialidad)

        return Response({
            "nombre": medico_obj.nombreCompleto,
            "especialidad": getattr(medico_obj.especialidad, "nombreEspecialidad", "Sin especialidad"),
            "porcentaje_ocupacion": porcentaje_ocupacion,
            "horas_por_semana": horas_por_semana_list,
            "box_mas_usado": box_mas_usado,
            "consultas_realizadas": consultas_realizadas,
            "uso_por_especialidad": uso_especialidad_dict,
        })
    

