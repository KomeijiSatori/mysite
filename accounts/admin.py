from django.contrib import admin
from .models import Profile, Notification, Follow

# Register your models here.


admin.site.register(Profile)
admin.site.register(Notification)
admin.site.register(Follow)
