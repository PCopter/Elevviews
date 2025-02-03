from django.contrib import admin
from .models import Camera, Photo

# Customizing the Camera admin panel
@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'connection_type', 'ip_address', 'added_on', 'updated_on')
    list_filter = ('status', 'connection_type', 'added_on')
    search_fields = ('name', 'ip_address', 'description')
    ordering = ('-added_on',)

# Customizing the Photo admin panel
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'camera', 'timestamp', 'photo_preview')
    list_filter = ('timestamp', 'camera')
    search_fields = ('camera__name', 'user__username')
    ordering = ('-timestamp',)

    # Displaying a preview of the photo in the admin panel
    def photo_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="width: 100px; height: auto;" />'
        return "No image available"
    photo_preview.allow_tags = True
    photo_preview.short_description = "Photo Preview"
