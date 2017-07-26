from django.db import models
from django.conf import settings

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # avatar =
    gender = models.CharField(blank=True, null=True, max_length=100, choices=(("male", "Male"), ("female", "Female")))
    birthday = models.DateField(blank=True, null=True)
    mobile = models.CharField(blank=True, null=True, max_length=100, help_text="Your mobile number")
    residence = models.CharField(blank=True, null=True, max_length=500, help_text="Where you live in")
    website = models.URLField(blank=True, null=True, help_text="Your personal website")
    microblog = models.CharField(blank=True, null=True, max_length=100, help_text="Your sina microblog")
    qq = models.CharField(blank=True, null=True, max_length=100, help_text="Your QQ number")
    wechat = models.CharField(blank=True, null=True, max_length=100, help_text="Your wechat id")
    introduction = models.TextField(null=True, blank=True, help_text="Something about yourself")

    def __str__(self):
        return str(self.user.username)

