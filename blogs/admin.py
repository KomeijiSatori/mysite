from django.contrib import admin

# Register your models here.

from .models import Blog, BlogCategory, BlogComment, BlogNestedComment


admin.site.register(Blog)
admin.site.register(BlogCategory)
admin.site.register(BlogComment)
admin.site.register(BlogNestedComment)
