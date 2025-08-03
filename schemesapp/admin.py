from django.contrib import admin
from .models import Feedback, Notification, Scheme, UserDetails, Application
# Register your models here.
admin.site.register(Feedback)
admin.site.register(Notification)
admin.site.register(Scheme)
admin.site.register(UserDetails)
admin.site.register(Application)