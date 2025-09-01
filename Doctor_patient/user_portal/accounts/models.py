from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPES = [
        ("Patient", "Patient"),
        ("Doctor", "Doctor"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
