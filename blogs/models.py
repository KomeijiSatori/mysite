from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=500, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publish_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_update_time = models.DateTimeField(null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-publish_time', 'title', 'author',)


class Comment(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publish_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_update_time = models.DateTimeField(null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        return self.text

    """
    rebuild order by running following command in the django shell
    from blogs.models import Comment
    Comment.objects.rebuild()
    """
    class MPTTMeta:
        order_insertion_by = ['-publish_time']


class BlogCategory(models.Model):
    blog = models.ManyToManyField(Blog)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
