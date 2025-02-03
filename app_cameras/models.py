from django.db import models
from django.conf import settings

# Create your models here.
class Camera(models.Model):

    
    # ชื่อหรือรหัสของกล้อง
    name = models.CharField(max_length=100, unique=True)
    name_thai = models.CharField(max_length=100, unique=True,blank=True, null=True)

    image = models.CharField(max_length=100, null=True, blank=True)

    # พิกัดตำแหน่งของกล้อง (ละติจูดและลองจิจูด)
    latitude = models.FloatField()
    longitude = models.FloatField()

    # สถานะของกล้อง (ออนไลน์/ออฟไลน์)
    status = models.CharField(max_length=10, choices=[('Online', 'Online'), ('Offline', 'Offline')], default='Offline')

    # ประเภทของการเชื่อมต่อ (Wi-Fi, Ethernet, MQTT, WebSocket)
    CONNECTION_TYPES = [
        ('Wi-Fi', 'Wi-Fi'),
        ('Ethernet', 'Ethernet'),
        ('MQTT', 'MQTT'),
        ('WebSocket', 'WebSocket'),
    ]
    connection_type = models.CharField(max_length=20, choices=CONNECTION_TYPES)

    # ที่อยู่ IP หรือ URL สำหรับเชื่อมต่อกล้อง
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    # วันที่และเวลาที่เพิ่มกล้องเข้าระบบ
    added_on = models.DateTimeField(auto_now_add=True)

    # วันที่และเวลาที่แก้ไขข้อมูลล่าสุด
    updated_on = models.DateTimeField(auto_now=True)

    # เพิ่มฟิลด์ QR Code
    qr_code = models.CharField(max_length=255, unique=True )  

    def __str__(self):
        return self.name


# Model สำหรับเก็บข้อมูลรูปภาพที่ถูกถ่าย
class Photo(models.Model):
    # เชื่อมโยงรูปภาพกับuser
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # เชื่อมโยงรูปภาพกับกล้อง
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    # ไฟล์รูปภาพที่ถูกอัพโหลด media/photos
    image = models.ImageField(upload_to='user_photos/')
    # เวลาและวันที่ที่ถ่ายภาพ
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo by {self.user.username} from {self.camera.name} on {self.timestamp}"