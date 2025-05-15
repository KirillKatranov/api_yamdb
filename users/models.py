# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    bio = models.TextField(blank=True)
    ROLE_CHOICES = (
    ("user", "User"),
    ("moderator", "Moderator"),
    ("admin", "Admin"),
    )
    
    

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="user",
    )