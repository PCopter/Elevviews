from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from .models import Camera, Photo
from app_users.models import CustomUser
import boto3
import json
import os
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import os
from dotenv import load_dotenv

load_dotenv()

# AWS IoT Core Configuration


# AWS Boto3 IoT Data Client
iot_client = boto3.client('iot-data',   region_name='ap-southeast-1', 
                      aws_access_key_id= os.getenv("AWS_ACCESS_KEY") ,
                      aws_secret_access_key= os.getenv("AWS_SECRET_KEY") )


def cameras(request):
    all_cameras = Camera.objects.all()
    context = {'cameras': all_cameras}
    return render(request, 'app_cameras/cameras.html', context)


def camera(request, camera_id):
    one_camera = get_object_or_404(Camera, id=camera_id)
    context = {'camera': one_camera}
    return render(request, 'app_cameras/camera.html', context)



from datetime import datetime



@login_required
def take_photo(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id)
    latest_photo = Photo.objects.filter(user=request.user).order_by('-timestamp').first()

    if request.method == 'POST':
        try: 
            # สั่งกล้องให้ถ่ายภาพผ่าน AWS IoT Core
            # ดึง user_id
            user_id = request.user.id

            # สร้างชื่อรูปภาพที่ไม่ซ้ำ
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            unique_image_name = f"{user_id}_{camera_id}_{timestamp}.jpg"

            # พารามิเตอร์สำหรับคำสั่งถ่ายรูป
            params = {
                "user_id": user_id,
                "camera_id": camera_id,
                "image_name": unique_image_name
            }

            shadow_payload = {
                "state": {
                    "desired": {
                        "camera": {
                            "action": "capture_image",
                            "params": params
                        }
                    }
                }
            }
            response = iot_client.update_thing_shadow(
                thingName=os.getenv("THING_NAME"),
                payload=json.dumps(shadow_payload)
            )

            # ตรวจสอบสถานะของคำสั่ง
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                message = 'Camera triggered successfully! This is the picture that was taken and has been saved in the database. They can be deleted or saved through your dashboard.'
            else:
                message = 'Failed to trigger the camera.'

            return JsonResponse({'message': message })

        except Exception as e:
            return JsonResponse({'error': str(e)})

    context = {
        'camera': camera,
        'latest_photo': latest_photo,  # ส่งรูปภาพล่าสุดไปยังเทมเพลต
    }
    return render(request, 'app_cameras/takephoto.html', context)




# ปิดการตรวจสอบ CSRF สำหรับ Raspberry Pi
@csrf_exempt  # ใช้เฉพาะในระหว่างการพัฒนา
def upload_photo(request):
    if request.method == 'POST' and request.FILES.get('image'):
        camera_id = request.POST.get('camera_id')
        user_id = request.POST.get('user_id')

        # ตรวจสอบว่ากล้องและผู้ใช้มีอยู่หรือไม่
        camera = Camera.objects.filter(id=camera_id).first()
        if not camera:
            return JsonResponse({'error': 'Camera not found'}, status=404)

        # บันทึกข้อมูลรูปภาพ
        photo = Photo.objects.create(
            user_id=user_id,
            camera=camera,
            image=request.FILES['image']
        )
        photo.save()

        return JsonResponse({'message': 'Photo uploaded successfully!', 'photo_id': photo.id})

    return JsonResponse({'error': 'Invalid request'}, status=400)




