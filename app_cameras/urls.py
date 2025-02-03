from django.urls import path
from . import views
from django.conf.urls.static import static
from project import settings

urlpatterns = [
    path('', views.cameras, name='cameras'),
    path('<int:camera_id>', views.camera, name='camera'),
    path('<int:camera_id>/takephoto/', views.take_photo, name='takephoto'),
    path('api/upload_photo/', views.upload_photo, name='upload_photo'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
