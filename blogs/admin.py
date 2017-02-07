from django.contrib import admin

# Register your models here.

from .models import User, Blog


admin.site.register(User)
admin.site.register(Blog)
