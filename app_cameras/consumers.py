import json
import cv2
import asyncio
from aiortc import RTCPeerConnection, MediaStreamTrack, RTCSessionDescription
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoStreamTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)  # ใช้กล้อง webcam (เปลี่ยนเป็นไฟล์หรือ RTSP ได้)

    async def recv(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        # แปลง OpenCV Frame เป็น WebRTC Frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame  # ส่งเฟรมวิดีโอไปยัง Client
    

class WebRTCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.pc = RTCPeerConnection()
        self.video_track = VideoStreamTrack()
        self.pc.addTrack(self.video_track)  # เพิ่มวิดีโอ track ลงใน WebRTC

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

    
