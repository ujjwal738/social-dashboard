from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Basic Info
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Social Media Tokens / Handles
    twitter_handle = models.CharField(max_length=100, blank=True)
    twitter_access_token = models.CharField(max_length=255, blank=True)
    twitter_access_secret = models.CharField(max_length=255, blank=True)

    facebook_handle = models.CharField(max_length=100, blank=True)
    facebook_access_token = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
