from django.db import models
from django.conf import settings

class User(models.Model):
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

    def __str__(self):
        return self.name