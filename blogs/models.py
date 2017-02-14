from django.db import models
from django.conf import settings
# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length = 500, null = False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    publish_time = models.DateTimeField(auto_now_add = True, auto_now = False)
    text = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-publish_time', 'title', 'author',)


class BlogCategory(models.Model):
    blog = models.ManyToManyField(Blog)
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
