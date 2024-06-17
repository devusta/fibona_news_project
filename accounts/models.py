from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.urls import reverse


# Userga qo'shimcha fieldlar qo'shish: 1-usul - Override
class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)


# 2-usul - OneToOne Model
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='accounts/profile_pics', blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} profile"
