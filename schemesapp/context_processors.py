from .models import Notification, Application

def global_user_context(request):
    """
    Provides global context variables across all templates for authenticated citizens and employees.
    """
    if not request.user.is_authenticated:
        return {
            'notifications': [],
            'unread_notifications_count': 0,
            'user_applications_count': 0,
            'user_is_employee': False,
        }

    is_emp = request.user.is_superuser or request.user.groups.filter(name='Employee').exists()
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:8]
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    if is_emp:
        apps_count = Application.objects.filter(status='pending').count()
    else:
        apps_count = Application.objects.filter(user=request.user).count()

    return {
        'notifications': notifications,
        'unread_notifications_count': unread_count,
        'user_applications_count': apps_count,
        'user_is_employee': is_emp,
    }
