import json
from channels.generic.websocket import AsyncWebsocketConsumer

class WebRTCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'offer':
            # รับ WebRTC Offer และส่ง Answer กลับไป
            await self.send(json.dumps({
                'type': 'answer',
                'sdp': 'Your WebRTC SDP Answer'
            }))