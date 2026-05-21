# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    # ONBOARDING SYSTEM
    is_onboarded = models.BooleanField(default=False)

    onboarding_step = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.username


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    github_username = models.CharField(max_length=100, blank=True)

    github_url = models.URLField(max_length=200, blank=True)

    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)