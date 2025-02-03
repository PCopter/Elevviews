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


@login_required
def dashboard(request: HttpRequest):
    user_photos = Photo.objects.filter(user=request.user).order_by('-timestamp')  # รูปภาพของผู้ใช้ เรียงตามเวลาล่าสุด
    return render(request, "app_users/dashboard.html", {'user_photos': user_photos})

@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id, user=request.user)
    
    if request.method == 'POST':
        photo.image.delete()  # ลบไฟล์จากระบบ
        photo.delete()        # ลบข้อมูลจากฐานข้อมูล
        return redirect('dashboard')  # กลับไปหน้า Dashboard

    return redirect('dashboard')


@login_required
def profile(request : HttpRequest):
    user = request.user
    # POST
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        is_new_profile = False

        try:
            # Create
            extended_form = ExtendedProfileForm(request.POST, instance=user.profile)
        except:
            # Update
            extended_form = ExtendedProfileForm(request.POST)
            is_new_profile = True



        if form.is_valid() and extended_form.is_valid():
            form.save()
            # Create
            if is_new_profile:
                profile = extended_form.save(commit=False)
                profile.user = user
                profile.save()
            # Update
            else:
                extended_form.save()
            return HttpResponseRedirect(reverse("profile"))
    
    else:
        form = UserProfileForm(instance=user)
        try:
            extended_form =  ExtendedProfileForm(instance=user.profile)
        except:
            extended_form =  ExtendedProfileForm()
    # GET
    
    context = {
        "form" : form,
        "extended_form" : extended_form,
    }
    return render(request, "app_users/profile.html", context)