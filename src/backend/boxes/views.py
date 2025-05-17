import json, time
from django.utils import timezone
from datetime import datetime
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Box
from .management.helpers.services import (
    get_boxes_with_kpis,
    get_box_franjas,
    calcular_porcentaje_ocupacion,
    )

# Detalle del box, muestra franjas horarias y ocupación
class BoxDetalleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, idBox):
        date_str = request.GET.get("date")
        if date_str:
            fecha = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            fecha = timezone.localdate()

        try:
            box = Box.objects.select_related("disponibilidadBox", "pasillo").get(idBox=idBox)
        except Box.DoesNotExist:
            return Response({"error": "Box no encontrado"}, status=404)

        franjas = get_box_franjas(box, fecha)
        porcentaje_ocupacion = calcular_porcentaje_ocupacion(franjas)

        return Response({
            "idBox": box.idBox,
            "numeroBox": box.idBox,
            "pasillo": box.pasillo.nombrePasillo,
            "franjas": franjas,
            "porcentajeOcupacion": porcentaje_ocupacion,
        })


# SSE para dashboard (boxes en tiempo real)
def boxes_stream(request):    
    date_str = request.GET.get("date")
    if date_str:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        target_date = timezone.localdate()

    def event_stream():
        while True:
            data = get_boxes_with_kpis(target_date)
            # print(f"Data: {data}")  # debug
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(2)  # Puedes ajustar el refresco

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    return response
