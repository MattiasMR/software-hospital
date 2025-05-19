# boxes/views.py
from collections import defaultdict

import json, time
from datetime import datetime, timedelta
from typing import Callable, Iterator, List

from django.http import StreamingHttpResponse
from django.utils import timezone
from django.utils.dateparse import parse_date
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Box
from .serializers import BoxDetalleSerializer, BoxStatusSimpleSerializer
from .management.services.helpers import (  # ←  nuevo path
    calcular_porcentaje_ocupacion,
    get_box_franjas,
    get_boxes_with_kpis,
)

REFRESH_SECONDS = 2  # poll interno SSE


# ──────────────────────────────────────────────────────────────────────
#   Dashboard en tiempo real (Server-Sent Events)
# ──────────────────────────────────────────────────────────────────────
def _sse_stream(generator_fn: Callable[[], Iterator[dict]]) -> StreamingHttpResponse:
    """
    Envuelve un generador de dicts en un flujo SSE.
    Maneja reconexión básica (retry) y content-type adecuado.
    """
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
    """Genera continuamente el snapshot de boxes con sus KPIs."""
    while True:
        yield get_boxes_with_kpis(target_date)
        time.sleep(REFRESH_SECONDS)


def boxes_stream(request):
    """
    Endpoint SSE consumido por el front (useBoxesSSE).
    Acepta ?date=YYYY-MM-DD para “congelar” el tablero en otro día.
    """
    date_str = request.GET.get("date")
    target_date = (
        datetime.strptime(date_str, "%Y-%m-%d").date()
        if date_str else timezone.localdate()
    )
    return _sse_stream(lambda: _boxes_generator(target_date))


# ──────────────────────────────────────────────────────────────────────
#   Detalle de un Box (franjas + % ocupación)
# ──────────────────────────────────────────────────────────────────────
class BoxDetalleView(APIView):
    """
    GET /api/boxes/<idBox>/detalle/?date=YYYY-MM-DD
    Devuelve las franjas horarias y % de ocupación para el Box indicado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, idBox: int):
        # 1️⃣ Fecha objetivo
        date_str = request.GET.get("date")
        fecha = (
            datetime.strptime(date_str, "%Y-%m-%d").date()
            if date_str else timezone.localdate()
        )

        # 2️⃣ Obtenemos el Box filtrando por 'id', no por 'idBox'
        try:
            box = Box.objects.select_related("disponibilidadBox", "pasillo").get(id=idBox)
        except Box.DoesNotExist:
            return Response({"detail": "Box no encontrado."}, status=404)

        # 3️⃣ Calculamos franjas y porcentaje mediante helpers
        franjas = get_box_franjas(box, fecha)
        porcentaje = calcular_porcentaje_ocupacion(franjas)

        # 4️⃣ Preparamos el payload exacto que espera el serializer
        payload = {
            "pasillo": box.pasillo.nombrePasillo,
            "franjas": franjas,
            "porcentajeOcupacion": porcentaje,
        }

        # 5️⃣ Serializamos y respondemos
        serializer = BoxDetalleSerializer(payload)
        return Response(serializer.data)

# ──────────────────────────────────────────────────────────────────────
#   Snapshot (HTTP) de todos los boxes para una fecha
#   – útil para export, reportes o fallback si falla SSE –
# ──────────────────────────────────────────────────────────────────────
class BoxStatusListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_str = request.GET.get("date")
        target_date = (
            datetime.strptime(date_str, "%Y-%m-%d").date()
            if date_str else timezone.localdate()
        )
        data = get_boxes_with_kpis(target_date)
        return Response(BoxStatusSimpleSerializer(data, many=True).data)
    

class ReportesView(APIView):
    """
    GET /api/boxes/reportes/?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
    Devuelve:
      - porcentaje_ocupacion: promedio diario de ocupación %
      - medicos_por_franja: dict { "08:00-09:00": total_slots, ... }
      - uso_por_especialidad: dict { "Pediatría": total_slots, ... }
      - medico_lider: { name, horas }
      - box_mayor_uso: { id, horas }
      - especialidad_mas_demanda: { name, horas }
      - ranking_boxes: [ { id, horas }, ... ] (top 5)
    """
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
            # 1) snapshot for global occupancy
            snapshot = get_boxes_with_kpis(day)
            if snapshot:
                total_days += 1
                # avg occupancy that day
                sum_ocup += sum(b["porcentajeOcupacion"] for b in snapshot) / len(snapshot)

            # 2) for each box we drill into its franjas for that day
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

        # build the final report
        porcentaje_ocupacion = round(sum_ocup / total_days, 2) if total_days else 0

        # medico líder
        if doctor_hours:
            name, hrs = max(doctor_hours.items(), key=lambda x: x[1])
        else:
            name, hrs = "—", 0
        medico_lider = {"name": name, "horas": hrs}

        # box mayor uso
        if box_hours:
            bid, bhrs = max(box_hours.items(), key=lambda x: x[1])
        else:
            bid, bhrs = None, 0
        box_mayor_uso = {"id": bid, "horas": bhrs}

        # especialidad más demanda
        if uso_por_especialidad:
            spec_name, spec_hrs = max(uso_por_especialidad.items(), key=lambda x: x[1])
        else:
            spec_name, spec_hrs = "—", 0
        especialidad_mas_demanda = {"name": spec_name, "horas": spec_hrs}

        # ranking de boxes (top 5)
        ranking = sorted(box_hours.items(), key=lambda x: x[1], reverse=True)[:5]
        ranking_boxes = [{"id": bid, "horas": hrs} for bid, hrs in ranking]

        # ranking de medicos (top 5)
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