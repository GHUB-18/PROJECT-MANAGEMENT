import uuid
from django.db import models
from django.conf import settings
from django.urls import reverse

class Project(models.Model):

    COLOR_CHOICES = [
        ('purple', 'Purple'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('orange', 'Orange'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    color_theme = models.CharField(
        max_length=20,
        choices=COLOR_CHOICES,
        default='purple'
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='projects'
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )

    invite_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_invite_link(self):
        return reverse('join_project', args=[self.invite_token])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title