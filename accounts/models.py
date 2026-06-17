from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    profile_picture = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True
    )
    job_title = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    is_onboarded = models.BooleanField(default=False)
    onboarding_step = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    github_username = models.CharField(max_length=100, blank=True)
    github_url = models.URLField(max_length=200, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# REMOVED: Duplicate/recursive signal receivers are gone to prevent runtime thread locking.