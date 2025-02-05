import json
from channels.generic.websocket import AsyncWebsocketConsumer
from aiortc import RTCSessionDescription, RTCPeerConnection

class WebRTCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.pc = RTCPeerConnection()  # ✅ สร้าง PeerConnection ที่นี่

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'offer':
            # รับ WebRTC Offer
            offer_sdp = data['sdp']
            offer = RTCSessionDescription(sdp=offer_sdp, type='offer')

            # ตั้ง RemoteDescription จาก Offer ที่ได้รับ
            await self.pc.setRemoteDescription(offer)

            # ✅ สร้าง Answer
            answer = await self.pc.createAnswer()
            await self.pc.setLocalDescription(answer)  # ✅ ตั้งค่า LocalDescription

            # ✅ ส่ง SDP Answer กลับไป
            await self.send(json.dumps({
                'type': 'answer',
                'sdp': self.pc.localDescription.sdp
            }))

    async def disconnect(self, close_code):
        if hasattr(self, "pc"):
            await self.pc.close()

    
