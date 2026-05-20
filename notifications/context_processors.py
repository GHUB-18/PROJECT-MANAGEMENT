# app/context_processors.py
from .models import Notification

def notifications_context(request):
    if request.user.is_authenticated:
        notes = Notification.objects.filter(user=request.user, is_read=False)
        return {'notifications': notes}
    return {}
