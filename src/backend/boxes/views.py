
import json
import time
from .models import Box
from django.http import StreamingHttpResponse
from rest_framework import generics, permissions
from django.views.decorators.http import condition
from .serializers import BoxStatusSerializer, BoxDetailSerializer


class BoxStatusListView(generics.ListAPIView):
    """
    GET /api/boxes/status/
    Lista estado actual de todos los boxes.
    """
    queryset = Box.objects.select_related('tipoBox', 'disponibilidadBox').all()
    serializer_class = BoxStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

class BoxDetailView(generics.RetrieveAPIView):
    """
    GET /api/boxes/{id}/detail/
    Devuelve detalle de box + sus consultas (agendas).
    """
    queryset = Box.objects.prefetch_related('consultas__medico', 'consultas__estadoConsulta').all()
    serializer_class = BoxDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'idBox'

def boxes_stream(request):
    def event_stream():
        while True:
            # Obtén tus boxes con sus relaciones
            qs = Box.objects.select_related('tipoBox', 'disponibilidadBox').all()
            data = [
                {
                    "idBox": b.idBox,
                    "numeroBox": b.numeroBox,
                    "tipoBox": b.tipoBox.tipoBox,
                    "disponibilidad": b.disponibilidadBox.disponibilidad
                }
                for b in qs
            ]
            # SSE manda esta línea con “data: JSON\n\n”
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(1)  # poll interno cada 5s (puedes subir a 10s o eliminar y usar signals)
    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")