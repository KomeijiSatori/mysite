from django.db import models
from django.conf import settings

# Create your models here.


class MineScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    play_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    time_spent = models.IntegerField(null=False)

    max_score_count = 15

    def __str__(self):
        return str(self.user) + " " + str(self.time_spent)

    class Meta:
        ordering = ('time_spent', 'play_time', 'user')
