from django.contrib import admin
from app_users.models import CustomUser, Profile, DataEngagement  # นำเข้า Profile และ DataEngagement
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.db.models import Count

admin.site.register(CustomUser, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'ages', 'nationality')  # เปลี่ยนจาก phone, address เป็น ages, nationality
    search_fields = ('user__username', 'ages', 'nationality')

@admin.register(DataEngagement)
class DataEngagementAdmin(admin.ModelAdmin):
    list_display = ('profile', 'photo', 'timestamp')
    search_fields = ('profile__user__username', 'photo__id')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)
    actions = ["show_statistics"]

    def show_statistics(self, request, queryset):
        total = queryset.count()
        
        # นับจำนวนแต่ละตัวเลือก
        reason_counts = DataEngagement.objects.values('reasons_for_visit').annotate(count=Count('id'))
        travel_counts = DataEngagement.objects.values('travel_with').annotate(count=Count('id'))
        satisfaction_counts = DataEngagement.objects.values('location_satisfaction').annotate(count=Count('id'))

        msg = f"📊 Total Responses: {total}\n\n"

        msg += "📌 **Reasons for Visit:**\n"
        for item in reason_counts:
            msg += f" - {item['reasons_for_visit']}: {item['count']} responses\n"

        msg += "\n🚶 **Travel With:**\n"
        for item in travel_counts:
            msg += f" - {item['travel_with']}: {item['count']} responses\n"

        msg += "\n😊 **Satisfaction Ratings:**\n"
        for item in satisfaction_counts:
            msg += f" - {item['location_satisfaction']}: {item['count']} responses\n"

        self.message_user(request, msg, level=messages.INFO)

    show_statistics.short_description = "Show Survey Statistics"
