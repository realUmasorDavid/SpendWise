# notifications/context_processors.py
from .models import Notification

def notification_context(request):
    if request.user.is_authenticated:
        return {
            'notifications': Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:5],
            'unread_count': Notification.objects.filter(user=request.user, is_read=False).count()
        }
    return {}