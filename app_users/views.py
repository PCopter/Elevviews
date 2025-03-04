# views.py
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from app_users.forms import UserProfileForm, ExtendedProfileForm, SignupForm
from app_users.models import CustomUser
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from app_users.utils.activation_token_generator import activation_token_generator
from app_cameras.models import Photo
from django.shortcuts import get_object_or_404, redirect
import boto3
from django.conf import settings
from urllib.parse import urlparse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


def signup(request: HttpRequest):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user: CustomUser = form.save(commit=False)
            user.is_active = False
            user.save()

            #login(request, user)

            # Build email html
            context = {
                "protocol": request.scheme,
                "host": request.get_host(),
                "uidb64": urlsafe_base64_encode(force_bytes(user.id)),
                "token": activation_token_generator.make_token(user),

            }
            email_body = render_to_string("app_users/activate_email.html",context=context)

            # Send email
            email = EmailMessage(
                to = [user.email], 
                subject="Activate your account",
                body = email_body,
                                 )
            email.send()
            return HttpResponseRedirect(reverse("signup_thankyou"))
    else:
        form = SignupForm()
    
    # Get        
    
    context = {"form" : form}
    return render(request, "app_users/signup.html", context)


def signup_thankyou(request : HttpRequest):
    return render(request, "app_users/signup_thankyou.html")


def activate(request : HttpRequest, uidb64: str, token:str):
    title = "Activate account done"
    description = "You can now log in."

    id = urlsafe_base64_decode(uidb64).decode()

    try:
        user: CustomUser = CustomUser.objects.get(id=id)
        if not activation_token_generator.check_token(user, token):
            raise Exception("Check token false")
        user.is_active = True
        user.save()
    except:
        print("Activate failed")
        title = "Activate account faild"
        description = "The link may be already in use or expired."

    context = { "title": title, "description": description }
    return render(request, "app_users/activate.html", context)


from app_users.models import DataEngagement,Profile

@login_required
def dashboard(request):
    user_photos = Photo.objects.filter(user=request.user).order_by('-timestamp')
    
    context = {
        'user_photos': user_photos,
        'REASON_CHOICES': DataEngagement.REASON_CHOICES,
        'TRAVEL_WITH_CHOICES': DataEngagement.TRAVEL_WITH_CHOICES,
        'SATISFACTION_CHOICES': DataEngagement.SATISFACTION_CHOICES,
        'PLANNING_CHOICES': DataEngagement.PLANNING_CHOICES,
    }

    return render(request, "app_users/dashboard.html", context)


@login_required
def save_engagement(request):
    if request.method == "POST":
        photo = get_object_or_404(Photo, id=request.POST.get("photo_id"))
        profile = get_object_or_404(Profile, user=request.user)

        location_satisfaction = request.POST.get("location_satisfaction")
        elevview_satisfaction = request.POST.get("elevview_satisfaction")

        engagement = DataEngagement.objects.create(
            photo=photo,
            profile=profile,
            reasons_for_visit=request.POST.getlist("reasons_for_visit"),
            travel_with=request.POST.get("travel_with", ""),  # ใส่ค่า default เป็น "" เพื่อป้องกัน KeyError
            location_satisfaction=int(location_satisfaction) if location_satisfaction.isdigit() else None,
            elevview_satisfaction=int(elevview_satisfaction) if elevview_satisfaction.isdigit() else None,
            planning_ahead=request.POST.get("planning_ahead", ""),
            location_comment=request.POST.get("location_comment", ""),
            elevview_comment=request.POST.get("elevview_comment", "")
        )

        

        return JsonResponse({
            "success": True,
            "download_url": photo.image
        })

    return JsonResponse({"success": False}, status=400)


@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id, user=request.user)

    if request.method == 'POST':
        # ถ้าใช้ S3 ต้องลบรูปจาก bucket ก่อน
        if settings.USE_S3:
            s3 = boto3.client('s3')
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            
            # ดึงชื่อไฟล์จาก URL
            parsed_url = urlparse(photo.image)
            file_key = parsed_url.path.lstrip('/')  # เอา path โดยไม่เอา `/`
            
            try:
                s3.delete_object(Bucket=bucket_name, Key=file_key)
            except Exception as e:
                print(f"Error deleting from S3: {e}")

        # ลบข้อมูลออกจากฐานข้อมูล
        photo.delete()
        
        return redirect('dashboard')  

    return redirect('dashboard')


# ✅ View สำหรับ login เสร็จแล้ว redirect ตามเงื่อนไข
@login_required
def login_redirect(request: HttpRequest):
    user = request.user
    # ถ้ามี profile แล้วไป home ถ้าไม่มีไป profile
    if hasattr(user, 'profile'):
        return redirect('home')
    else:
        return redirect('profile')


# ✅ View สำหรับหน้า profile
@login_required
def profile(request: HttpRequest):
    user = request.user
    is_new_profile = not hasattr(user, 'profile')  # True ถ้ายังไม่มี profile

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)

        # ถ้ามี profile ใช้ instance เดิม ถ้าไม่มีสร้างใหม่
        extended_form = ExtendedProfileForm(
            request.POST, instance=getattr(user, 'profile', None)
        )

        if form.is_valid() and extended_form.is_valid():
            form.save()
            profile = extended_form.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect(reverse("home"))  # กลับไป home หลังบันทึกสำเร็จ
    else:
        form = UserProfileForm(instance=user)
        extended_form = ExtendedProfileForm(instance=getattr(user, 'profile', None))

    context = {
        "form": form,
        "extended_form": extended_form,
        "is_new_profile": is_new_profile,  # ส่งไปให้ template
    }
    return render(request, "app_users/profile.html", context)