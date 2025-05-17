import json
from datetime import datetime
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from boxes.models import Box, Consulta
from .management.helpers.services import get_boxes_with_kpis, get_reportes_kpis

# Endpoint REST para boxes (estado actual + KPIs)
class BoxStatusListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_str = request.GET.get("date")
        from datetime import datetime
        from django.utils import timezone

        if date_str:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            target_date = timezone.localdate()

        data = get_boxes_with_kpis(target_date)
        return Response(data)
    
# Endpoint REST para KPIs
class ReporteKPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_from      = request.GET.get("date_from")
        date_to        = request.GET.get("date_to")
        especialidad   = request.GET.get("especialidad")

        # Intenta parsear fechas
        from datetime import datetime
        df, dt = None, None
        try:
            if date_from:
                df = datetime.strptime(date_from, "%Y-%m-%d").date()
            if date_to:
                dt = datetime.strptime(date_to, "%Y-%m-%d").date()
        except Exception:
            pass  # Si falla, será None y el helper usa fecha de hoy

        data = get_reportes_kpis(df, dt, especialidad)
        return Response(data)

class BoxDetailView(APIView):
    permission_classes = [IsAuthenticated]  # si quieres protegerlo

    def get(self, request, idBox):
        # Por defecto muestra las franjas de hoy, puedes cambiarlo por query param
        date_str = request.GET.get("date")
        if date_str:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            from django.utils import timezone
            date = timezone.localdate()

        try:
            box = Box.objects.get(idBox=idBox)
        except Box.DoesNotExist:
            return Response({"error": "Box no encontrado"}, status=404)

        consultas = Consulta.objects.filter(box=box, fechaHoraInicio__date=date).select_related("medico", "estadoConsulta").order_by("fechaHoraInicio")
        franjas = [
            {
                "inicio": c.fechaHoraInicio.strftime("%H:%M"),
                "fin": c.fechaHoraFin.strftime("%H:%M"),
                "estado": c.estadoConsulta.estadoConsulta,
                "medico": c.medico.nombreCompleto if c.medico else None,
            }
            for c in consultas
        ]

        total = consultas.count()
        ocupadas = consultas.filter(estadoConsulta__estadoConsulta='Ocupado').count()
        porcentaje_ocupacion = int((ocupadas / total) * 100) if total else 0

        data = {
            "idBox": box.idBox,
            "numeroBox": getattr(box, "numeroBox", box.idBox),
            "tipoBox": box.tipoBox.tipoBox,
            "disponibilidad": box.disponibilidadBox.disponibilidad,
            "pasillo": box.pasillo.nombrePasillo,
            "porcentajeOcupacion": porcentaje_ocupacion,  # <-- AGREGA ESTO!
            "franjas": franjas,
        }
        return Response(data)

def boxes_stream(request):
    import time
    from django.utils import timezone

    date_str = request.GET.get("date")
    if date_str:
        from datetime import datetime
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        target_date = timezone.localdate()

    def event_stream():
        while True:
            data = get_boxes_with_kpis(target_date)
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(2)

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    return response
