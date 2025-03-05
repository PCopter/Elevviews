from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from .models import Camera, Photo
import boto3
import json
import os
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth import get_user_model
import time

# AWS IoT Core Configuration
AWS_REGION = 'ap-southeast-1'
AWS_ENDPOINT = 'your-endpoint.amazonaws.com'
THING_NAME = "RaspPiCam"  # ชื่อ Thing ใน AWS IoT

# AWS Boto3 IoT Data Client
iot_client = boto3.client('iot-data',   region_name='ap-southeast-1', 
                      aws_access_key_id= settings.AWS_ACCESS_KEY ,
                      aws_secret_access_key= settings.AWS_SECRET_KEY )

# AWS Boto3 KVS Data Client
kvs_client = boto3.client(
    'kinesisvideo',
    region_name=settings.AWS_KVS_REGION_NAME,
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY
)


def get_kvs_credentials(request):
    # AWS Credentials
    access_key = ""
    secret_key = ""
    region = "ap-southeast-1"
    channel_arn = ""

    # Get Signaling Channel Endpoints
    kvs_client = boto3.client("kinesisvideo", region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    response = kvs_client.get_signaling_channel_endpoint(
        ChannelARN=channel_arn,
        SingleMasterChannelEndpointConfiguration={
            "Protocols": ["WSS", "HTTPS"],
            "Role": "VIEWER",
        },
    )

    endpoints = {e["Protocol"]: e["ResourceEndpoint"] for e in response["ResourceEndpointList"]}

    return JsonResponse({
        "accessKeyId": access_key,
        "secretAccessKey": secret_key,
        "region": region,
        "channelARN": channel_arn,
        "endpoints": endpoints,
    })

def webrtc_view(request):
    return render(request, "app_cameras/webrtc_viewer.html")



def get_data_endpoint(stream_name, api_name='GET_HLS_STREAMING_SESSION_URL'):
    response = kvs_client.get_data_endpoint(
        StreamName=stream_name,
        APIName=api_name
    )
    return response['DataEndpoint']

def get_hls_stream_url(stream_name):
    data_endpoint = get_data_endpoint(stream_name)
    archived_media_client = boto3.client(
        'kinesis-video-archived-media',
        endpoint_url=data_endpoint,
        region_name=settings.AWS_KVS_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_KEY
    )

    response = archived_media_client.get_hls_streaming_session_url(
        StreamName=stream_name,
        PlaybackMode='LIVE',
        HLSFragmentSelector={'FragmentSelectorType': 'PRODUCER_TIMESTAMP'}
    )
    return response['HLSStreamingSessionURL']



def cameras(request):
    all_cameras = Camera.objects.all()
    context = {'cameras': all_cameras}
    return render(request, 'app_cameras/cameras.html', context)


def camera(request, camera_id):
    one_camera = get_object_or_404(Camera, id=camera_id)
    context = {'camera': one_camera}
    return render(request, 'app_cameras/camera.html', context)


@login_required
def take_photo(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id)
    latest_photo = None

    # ดึง URL สตรีมจาก AWS KVS
    try:
        stream_url = get_hls_stream_url(settings.KINESIS_VIDEO_STREAM_NAME)
    except Exception as e:
        stream_url = None
    
    if request.method == 'POST':
        try: 
            user_id = request.user.id
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            unique_image_name = f"{user_id}_{camera_id}_{timestamp}"

            # รับค่าลายน้ำจาก request
            data = json.loads(request.body)
            watermark = data.get("watermark", "none")  # ค่า default เป็น "none"

            params = {
                "user_id": user_id,
                "camera_id": camera_id,
                "image_name": unique_image_name,
                "format": "jpg",
                "watermark": watermark,  # ส่งค่าลายน้ำไปที่ IoT Core
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
                thingName=THING_NAME,
                payload=json.dumps(shadow_payload)
            ) 

            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                # ดึงรูปจากฐานข้อมูลล่าสุด
                latest_photo = Photo.objects.filter(user_id=user_id, camera=camera).order_by('-id').first()
                if latest_photo:
                    return JsonResponse({'success': True, 'image_url': latest_photo.image})
                # else:
                #     return JsonResponse({'error': 'Image not found in database'})

        except Exception as e:
            return JsonResponse({'error': str(e)})

    context = {
        'camera': camera,
        'stream_url': stream_url,
        'latest_photo': latest_photo  # ส่งรูปล่าสุดไปที่ Template
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



User = get_user_model()

@csrf_exempt  # ปิดการตรวจสอบ CSRF (ใช้เฉพาะใน development)
def update_photo_db(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            user_id = data.get("user_id")
            camera_id = data.get("camera_id")
            image_url = data.get("image_url")

            # ตรวจสอบว่ามี user และ camera ในระบบหรือไม่
            user = User.objects.filter(id=user_id).first()
            camera = Camera.objects.filter(id=camera_id).first()

            if not user:
                return JsonResponse({"error": "User not found"}, status=404)
            if not camera:
                return JsonResponse({"error": "Camera not found"}, status=404)

            # บันทึกข้อมูลรูปภาพ
            photo = Photo.objects.create(
                user=user,
                camera=camera,
                image=image_url
            )

            return JsonResponse({"message": "Photo record created successfully!", "photo_id": photo.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

