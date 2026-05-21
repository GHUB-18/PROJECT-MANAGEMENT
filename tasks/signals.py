# tasks/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from notifications.models import Notification

@receiver(post_save, sender=Task)
def create_task_notification(sender, instance, created, **kwargs):
    if created and instance.assigned_to:
        Notification.objects.create(
            user=instance.assigned_to,
            message=f"New task assigned: {instance.title}",
            link=f"/tasks/{instance.id}/"
        )
