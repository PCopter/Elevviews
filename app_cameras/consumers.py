import json
from channels.generic.websocket import AsyncWebsocketConsumer
from aiortc import RTCSessionDescription

class WebRTCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'offer':
            # รับ WebRTC Offer
            offer_sdp = data['sdp']
            offer = RTCSessionDescription(sdp=offer_sdp, type='offer')

            # สร้าง Answer (ในกรณีนี้เราไม่ต้องการเสียง)
            answer = await pc.createAnswer({
                'offerToReceiveVideo': True,   # รับวิดีโอ
                'offerToReceiveAudio': False,  # ไม่รับเสียง
                'video': {
                    'width': 1920,
                    'height': 1080,
                    'frameRate': 30
                }
            })

            # ส่ง SDP Answer กลับไป
            await self.send(json.dumps({
                'type': 'answer',
                'sdp': answer.sdp
            }))