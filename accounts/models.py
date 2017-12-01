from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(blank=True, null=True, max_length=100, choices=(("male", "Male"), ("female", "Female")))
    birthday = models.DateField(blank=True, null=True, help_text="yyyy-mm-dd")
    mobile = models.CharField(blank=True, null=True, max_length=100, help_text="Your mobile number")
    residence = models.CharField(blank=True, null=True, max_length=500, help_text="Where you live in")
    website = models.URLField(blank=True, null=True, help_text="Your personal website")
    microblog = models.CharField(blank=True, null=True, max_length=100, help_text="Your sina microblog")
    qq = models.CharField(blank=True, null=True, max_length=100, help_text="Your QQ number")
    wechat = models.CharField(blank=True, null=True, max_length=100, help_text="Your wechat id")
    introduction = models.TextField(null=True, blank=True, help_text="Something about yourself")

    def __str__(self):
        return str(self.user.username)


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('Reply', 'Reply'),
        ('Subscribe', 'Subscribe'),
        ('At', 'At'),
    )

    unread = models.BooleanField(default=True)
    type = models.CharField(max_length=max([len(x[0]) for x in NOTIFICATION_TYPES]), choices=NOTIFICATION_TYPES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.type) + " from " + str(self.content_object)


class Follow(models.Model):
    fan = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="star")
    star = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="fan")

    def __str__(self):
        return str(self.star.username) + "<--" + str(self.fan.username)
