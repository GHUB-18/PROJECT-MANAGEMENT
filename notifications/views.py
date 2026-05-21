# app/views.py
from django.http import JsonResponse
from .models import Notification

def unread_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return JsonResponse({'count': count})
    return JsonResponse({'count': 0})

def notifications_list(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    else: 
        notifications = []
    return render(request, 'notifications/notifications_list.html', {'notifications': notifications})
    