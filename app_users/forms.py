# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from app_users.models import Profile ,CustomUser

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password", "class": "form-control"})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username", "class": "form-control"}),
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
        fields = ("ages", "nationality")
        widgets = {
            "ages": forms.TextInput(attrs={"placeholder": "Age", "class": "form-control", "min": 0}),
            "nationality": forms.TextInput(attrs={"placeholder": "Nationality", "class": "form-control"}),
        }

        # labels = {
        #     "ages": "อายุ",
        #     "nationality": "สัญชาติ",
        # }

from django import forms
from .models import DataEngagement  # นำเข้าโมเดลแบบสอบถาม

class DataEngagementForm(forms.ModelForm):
    class Meta:
        model = DataEngagement
        fields = ['reasons_for_visit', 'travel_with', 'location_satisfaction', 'location_comment', 
                  'elevview_satisfaction', 'elevview_comment', 'planning_ahead']
        widgets = {
            'reasons_for_visit': forms.CheckboxSelectMultiple(),
            'travel_with': forms.RadioSelect(),
            'location_satisfaction': forms.RadioSelect(),
            'elevview_satisfaction': forms.RadioSelect(),
            'planning_ahead': forms.RadioSelect(),
        }
