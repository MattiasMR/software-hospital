# boxes/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Box
import json

def broadcast_boxes():
    qs = Box.objects.select_related('tipoBox','disponibilidadBox').all()
    data = [
      {
        "idBox": b.idBox,
        "numeroBox": b.numeroBox,
        "tipoBox": b.tipoBox.tipoBox,
        "disponibilidad": b.disponibilidadBox.disponibilidad
      }
      for b in qs
    ]
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
      "boxes",
      {"type": "box_update", "data": data}
    )

@receiver([post_save, post_delete], sender=Box)
def on_box_change(sender, **kwargs):
    broadcast_boxes()
