from django.contrib.auth.models import User, AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

class Profile(models.Model):
    address = models.TextField(default="")
    phone = models.CharField(default="",max_length=15)
    user = models.OneToOneField("app_users.CustomUser", on_delete= models.CASCADE)
