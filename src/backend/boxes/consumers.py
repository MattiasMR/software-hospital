# boxes/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class BoxConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("boxes", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("boxes", self.channel_name)

    # Handler para mensajes de grupo tipo 'box_update'
    async def box_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))
