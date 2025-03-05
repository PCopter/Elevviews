from django.contrib import admin
from app_users.models import CustomUser, Profile, DataEngagement  # นำเข้า Profile และ DataEngagement
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.db.models import Count
from django.utils.html import format_html

admin.site.register(CustomUser, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'ages', 'nationality')  # เปลี่ยนจาก phone, address เป็น ages, nationality
    search_fields = ('user__username', 'ages', 'nationality')


class TravelWithFilter(admin.SimpleListFilter):
    title = 'Travel With'
    parameter_name = 'travel_with'

    def lookups(self, request, model_admin):
        return DataEngagement.TRAVEL_WITH_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(travel_with=self.value())
        return queryset

class LocationSatisfactionFilter(admin.SimpleListFilter):
    title = 'Location Satisfaction'
    parameter_name = 'location_satisfaction'

    def lookups(self, request, model_admin):
        return DataEngagement.SATISFACTION_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(location_satisfaction=self.value())
        return queryset


@admin.register(DataEngagement)
class DataEngagementAdmin(admin.ModelAdmin):
    list_display = ('profile', 'photo', 'timestamp', 
                    'count_reasons_for_visit', 'count_travel_with', 
                    'count_location_satisfaction', 'count_elevview_satisfaction', 
                    'count_planning_ahead')  # เพิ่มฟังก์ชันที่แสดงจำนวน
    
    search_fields = ('profile__user__username', 'photo__id')
    list_filter = ('timestamp', TravelWithFilter, LocationSatisfactionFilter)  # เพิ่ม filters
    ordering = ('-timestamp',)

    # นับจำนวนแต่ละตัวเลือกใน reasons_for_visit (JSONField)
    def count_reasons_for_visit(self, obj):
        if isinstance(obj.reasons_for_visit, list):
            return ", ".join(obj.reasons_for_visit)  # แสดงรายการที่เลือก
        return "No data"
    count_reasons_for_visit.short_description = "Reasons for Visit"

    # นับจำนวนแต่ละตัวเลือกของ travel_with
    def count_travel_with(self, obj):
        return dict(DataEngagement.TRAVEL_WITH_CHOICES).get(obj.travel_with, "Unknown")
    count_travel_with.short_description = "Travel With"

    # นับจำนวนระดับความพึงพอใจของ Location
    def count_location_satisfaction(self, obj):
        return f"{obj.location_satisfaction} ⭐"
    count_location_satisfaction.short_description = "Location Satisfaction"

    # นับจำนวนระดับความพึงพอใจของ Elevview
    def count_elevview_satisfaction(self, obj):
        return f"{obj.elevview_satisfaction} ⭐"
    count_elevview_satisfaction.short_description = "Elevview Satisfaction"

    # นับจำนวนของ Planning Ahead
    def count_planning_ahead(self, obj):
        return dict(DataEngagement.PLANNING_CHOICES).get(obj.planning_ahead, "Unknown")
    count_planning_ahead.short_description = "Planning Ahead"
