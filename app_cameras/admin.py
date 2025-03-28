from django.contrib import admin
from .models import Camera, Photo
from django.utils.html import format_html

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
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image)
        return "No image available"
   
    photo_preview.short_description = "Photo Preview"
