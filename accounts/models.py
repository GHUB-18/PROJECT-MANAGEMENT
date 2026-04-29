from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model to handle profile pictures and roles 
    as seen in the ProjectHub UI designs.
    """
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        null=True, 
        blank=True
    )
    job_title = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        help_text="e.g. UI/UX Designer or Backend Developer"
    )

    def __str__(self):
        return self.username