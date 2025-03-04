from django.contrib.auth.models import User, AbstractUser
from django.db import models




class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

class Profile(models.Model):
    ages = models.CharField(max_length=3, default="")  # ฟิลด์สำหรับอายุ
    nationality = models.CharField(max_length=50, default="")  # ฟิลด์สำหรับสัญชาติ
    user = models.OneToOneField("app_users.CustomUser", on_delete= models.CASCADE)

class DataEngagement(models.Model):
    # ความสัมพันธ์กับ Photo (หนึ่งรูปภาพสามารถมีหลาย engagement)
    photo = models.ForeignKey('app_cameras.Photo', on_delete=models.CASCADE, related_name='engagements')

    # ความสัมพันธ์กับ Profile (ผู้ใช้ที่ตอบแบบสอบถาม)
    profile = models.ForeignKey('app_users.Profile', on_delete=models.CASCADE, related_name='engagements')

    # คำถาม 1: เหตุผลหลักในการมาเยือน (เลือกได้มากกว่า 1)
    REASON_CHOICES = [
        ('nature', 'Beautiful nature and scenery'),
        ('activities', 'Interesting activities'),
        ('culture', 'Culture and history'),
        ('recommendations', 'Recommends from reviews'),
        ('convenience', 'Convenient location or easy access'),
        ('promotions', 'Special promotions or discounts'),
    ]
    reasons_for_visit = models.JSONField(default=list)  # เก็บเป็นลิสต์ของเหตุผล

    # คำถาม 2: มากับใคร
    TRAVEL_WITH_CHOICES = [
        ('alone', 'Alone'),
        ('family', 'With family'),
        ('friends', 'With friends'),
        ('tour_group', 'With a tour group'),
    ]
    travel_with = models.CharField(max_length=20, choices=TRAVEL_WITH_CHOICES)

    # คำถาม 3: ระดับความพึงพอใจสำหรับสถานที่
    SATISFACTION_CHOICES = [
        (1, '😡'),
        (2, '😞'),
        (3, '😑'),
        (4, '🙂'),
        (5, '😍'),
    ]
    location_satisfaction = models.IntegerField(choices=SATISFACTION_CHOICES)

    # คำถาม 4: ความคิดเห็นเพิ่มเติมสำหรับสถานที่ (ไม่จำเป็น)
    location_comment = models.TextField(blank=True, null=True)

    # คำถาม 5: ระดับความพึงพอใจสำหรับ Elevview
    elevview_satisfaction = models.IntegerField(choices=SATISFACTION_CHOICES)

    # คำถาม 6: ความคิดเห็นเพิ่มเติมสำหรับ Elevview (ไม่จำเป็น)
    elevview_comment = models.TextField(blank=True, null=True)

    # คำถาม 7: วางแผนล่วงหน้ากี่วัน
    PLANNING_CHOICES = [
        ('last_minute', 'No prior planning (last-minute decision)'),
        ('1_3_days', '1-3 days in advance'),
        ('1_4_weeks', '1-4 weeks in advance'),
        ('more_than_1_month', 'More than 1 month in advance'),
    ]
    planning_ahead = models.CharField(max_length=20, choices=PLANNING_CHOICES)

    # วันที่และเวลาที่ตอบแบบสอบถาม
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Engagement by {self.profile.user.username} for photo {self.photo.id}"