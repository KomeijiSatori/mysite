from django.db.models.signals import post_save, post_delete
from django.conf import settings

from .models import Profile
from .service import NotificationService
from blogs.models import Comment, Blog


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass


def post_save_comment_receiver(sender, instance, created, *args, **kwargs):
    if created:
        NotificationService.create_reply_notification(instance)
        NotificationService.create_at_notification(instance, instance.text)


def post_save_blog_receiver(sender, instance, created, *args, **kwargs):
    if created:
        NotificationService.create_subscribe_notification(instance)
        NotificationService.create_at_notification(instance, instance.text)


def post_delete_notification_receiver(sender, instance, *args, **kwargs):
    NotificationService.delete_notification(instance)


post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)
post_save.connect(post_save_comment_receiver, sender=Comment)
post_save.connect(post_save_blog_receiver, sender=Blog)
post_delete.connect(post_delete_notification_receiver, sender=Comment)
post_delete.connect(post_delete_notification_receiver, sender=Blog)
