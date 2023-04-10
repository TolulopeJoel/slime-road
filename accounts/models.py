from django.contrib.auth.models import AbstractUser
from django.db import models


class Creator(AbstractUser):
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )
    bio = models.TextField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='female')
    profile_picture = models.ImageField(upload_to='creator/%Y/%m/%d')
