from django.contrib import admin
from app_users.models import CustomUser, Profile, DataEngagement  # นำเข้า Profile และ DataEngagement
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'ages', 'nationality')  # เปลี่ยนจาก phone, address เป็น ages, nationality
    search_fields = ('user__username', 'ages', 'nationality')

@admin.register(DataEngagement)
class DataEngagementAdmin(admin.ModelAdmin):
    list_display = ('profile', 'photo', 'timestamp')  # เพิ่ม profile ให้ชัดเจนขึ้น
    search_fields = ('profile__user__username', 'photo__id')  # ค้นหาด้วยชื่อผู้ใช้หรือไอดีรูป
    list_filter = ('timestamp',)  # กรองตามวันที่
    ordering = ('-timestamp',)  # เรียงตามเวลาสร้างล่าสุด
