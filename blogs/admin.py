from django.contrib import admin
from mptt.admin import MPTTModelAdmin

# Register your models here.

from .models import Blog, BlogCategory, Comment, BlogDraft


admin.site.register(Blog)
admin.site.register(BlogCategory)
admin.site.register(Comment, MPTTModelAdmin)
admin.site.register(BlogDraft)
