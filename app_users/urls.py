from django.urls import path,include
from app_users import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("signup", view=views.signup, name = "signup"),
    path("signup/thankyou", view=views.signup_thankyou, name = "signup_thankyou"),
    path("activate/<str:uidb64>/<str:token>", view=views.activate, name = "activate"),
    path("dashboard", view=views.dashboard, name = "dashboard"),
    path("profile", view=views.profile, name = "profile"),
    path('delete-photo/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('login-redirect/', views.login_redirect, name='login_redirect'),
    path("save-engagement/", view=views.save_engagement, name="save_engagement"),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
] 



