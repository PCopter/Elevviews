from django.urls import path
from . import views
from django.conf.urls.static import static
from project import settings

urlpatterns = [
    path('', views.cameras, name='cameras'),
    path('<int:camera_id>', views.camera, name='camera'),
    path('<int:camera_id>/takephoto/', views.take_photo, name='takephoto'),
    path('api/upload_photo/', views.upload_photo, name='upload_photo'),
    path("get_kvs_credentials/", views.get_kvs_credentials, name="get_kvs_credentials"),
    path("webrtc_viewer/", views.webrtc_view, name="webrtc_viewer"),
    path("api/update-photo-db/", views.update_photo_db, name="update_photo_db"),
]

