from rest_framework import generics, permissions
from .models import Box
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
