from django.contrib import admin

# Register your models here.

from .models import Blog, BlogCategory


admin.site.register(Blog)
admin.site.register(BlogCategory)
