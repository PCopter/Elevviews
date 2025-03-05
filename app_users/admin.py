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
    list_display = ('profile', 'photo', 'timestamp', 'count_reasons', 'count_travel_with', 'count_satisfaction')
    search_fields = ('profile__user__username', 'photo__id')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)

    def count_reasons(self, obj):
        return len(obj.reasons_for_visit) if obj.reasons_for_visit else 0
    count_reasons.short_description = "Number of Reasons"

    def count_travel_with(self, obj):
        return obj.get_travel_with_display()  # แสดงตัวเลือกที่เลือก เช่น "With family"
    count_travel_with.short_description = "Travel With"

    def count_satisfaction(self, obj):
        return f"📍{obj.location_satisfaction} | 📷{obj.elevview_satisfaction}"
    count_satisfaction.short_description = "Satisfaction (Location | Elevview)"
