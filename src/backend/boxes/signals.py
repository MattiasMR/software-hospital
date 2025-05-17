from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Box

def broadcast_boxes():
    """
    Envía la lista completa de boxes por WebSocket si hay un channel_layer activo.
    """
    channel_layer = get_channel_layer()
    if not channel_layer:
        # Si no está configurado, salimos sin error
        return

    # Prepara payload (podrías serializar con tu Serializer)
    from .serializers import BoxSerializer
    data = BoxSerializer(Box.objects.all(), many=True).data

    async_to_sync(channel_layer.group_send)(
        "boxes_group",
        {
            "type": "boxes.update",
            "boxes": data,
        }
    )

@receiver(post_save, sender=Box)
@receiver(post_delete, sender=Box)
def on_box_change(sender, instance, **kwargs):
    broadcast_boxes()
