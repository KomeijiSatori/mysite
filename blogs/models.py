from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length = 16, null = False)
    password = models.CharField(max_length = 40, null = False)
    email = models.EmailField(null = False)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length = 50, null = True)
    author = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True)
    publish_time = models.DateTimeField(auto_now_add = True, auto_now = False)
    text = models.TextField()

    def __str__(self):
        return self.title + " by " + self.author + " at " + self.publish_time
