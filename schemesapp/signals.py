from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Scheme, UserDetails, Notification

@receiver(post_save, sender=Scheme)
def notify_users_on_new_scheme(sender, instance, created, **kwargs):
    if created:
        scheme = instance
        for user_detail in UserDetails.objects.all():
            eligible = scheme.is_user_eligible(user_detail)
            Notification.objects.create(
                user=user_detail.user,
                message=f"New scheme '{scheme.name}' added. You are {'eligible' if eligible else 'not eligible'}.",
                scheme=scheme,
                is_read=False,
            )
            print(f"Notifying users about: {scheme.name}")
