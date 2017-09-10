from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from .models import Profile, Notification
from blogs.models import Comment, Blog


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass


def post_save_comment_receiver(sender, instance, created, *args, **kwargs):
    if created:
        # for comment post to a blog
        if instance.parent is None and instance.blog.author != instance.author:
            Notification.objects.create(content_object=instance, user=instance.blog.author)
        # else if comment post to another comment
        elif instance.parent is not None and instance.parent.author != instance.author:
            Notification.objects.create(content_object=instance, user=instance.parent.author)


def post_save_blog_receiver(sender, instance, created, *args, **kwargs):
    if created:
        # send notification to all followers
        author = instance.author
        relations = author.fan.all()
        fans = [relation.fan for relation in relations]
        for fan in fans:
            Notification.objects.create(content_object=instance, user=fan)


def post_delete_notification_receiver(sender, instance, *args, **kwargs):
    ctype = ContentType.objects.get_for_model(instance)
    Notification.objects.filter(content_type=ctype).filter(object_id=instance.id).delete()


post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)
post_save.connect(post_save_comment_receiver, sender=Comment)
post_save.connect(post_save_blog_receiver, sender=Blog)
post_delete.connect(post_delete_notification_receiver, sender=Comment)
post_delete.connect(post_delete_notification_receiver, sender=Blog)