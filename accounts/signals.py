# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def handle_user_profile_sync(sender, instance, created, **kwargs):
    """Handles profile provisioning and save states safely without infinite recursion."""
    if created:
        Profile.objects.get_or_create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            # Using update fields or explicit checks ensures saving profile does not loop back
            instance.profile.save()

def user_signed_up(request, user, **kwargs):
    user.onboarding_step = 1
    user.is_onboarded = False
    user.save()