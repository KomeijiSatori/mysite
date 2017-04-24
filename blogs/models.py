from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe

from markdown_deux import markdown
# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=500, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publish_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    text = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-publish_time', 'title', 'author',)

    def get_markdown(self):
        content = self.text
        return mark_safe(markdown(content))



class BlogCategory(models.Model):
    blog = models.ManyToManyField(Blog)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publish_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    text = models.TextField()

    def __str__(self):
        return self.text


class BlogNestedComment(models.Model):
    blog_comment = models.ForeignKey(BlogComment, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publish_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    text = models.TextField()

    def __str__(self):
        return self.text
