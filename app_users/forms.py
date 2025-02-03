# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from app_users.models import Profile ,CustomUser

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("email",)

        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username", "class": "form-control"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"placeholder": "Confirm Password", "class": "form-control"}),
        }
    

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name")

         # เพิ่ม widget เพื่อให้ดูทันสมัย
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name", "class": "form-control"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name", "class": "form-control"}),
        }

class ExtendedProfileForm(forms.ModelForm):
    prefix = "extended"
    class Meta:
        model = Profile
        fields = ("address", "phone")
        widgets = {"address": forms.Textarea(attrs={"rows": 3})}

        widgets = {
            "address": forms.Textarea(attrs={"rows": 3, "placeholder": "Address", "class": "form-control"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone Number", "class": "form-control"}),
        }

        # labels = {
        #     "address": "ที่อยู่",
        #     "phone": "เบอร์โทรศัพท์",
        # }

