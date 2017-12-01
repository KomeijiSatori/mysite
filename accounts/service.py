import re

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from .models import Follow, Notification


class FollowService(object):
    @classmethod
    def add_fan_star(cls, fan, star):
        """
        Add a fan to a star
        :param fan: type: User, the fan user
        :param star: type: User, the star user
        :return: result: type: Bool, the result whether the relation is created
        """
        if fan is None or star is None:
            return False
        if not(isinstance(fan, User) and isinstance(star, User)):
            return False
        relation = Follow.objects.filter(star=star).filter(fan=fan)
        if len(relation) > 0:
            return False
        else:
            Follow.objects.create(star=star, fan=fan)
            return True

    @classmethod
    def remove_fan_star(cls, fan, star):
        """
        Remove a fan from a star
        :param fan: type: User, the fan user
        :param star: type: User, the star user
        :return: result: type: Bool, the result whether the relation is deleted
        """
        if fan is None or star is None:
            return False
        if not(isinstance(fan, User) and isinstance(star, User)):
            return False
        relation = Follow.objects.filter(star=star).filter(fan=fan)
        if len(relation) == 1:
            relation.delete()
            return True
        else:
            return False

    @classmethod
    def is_fan_star(cls, fan, star):
        """
        Judge if there is a fan-star relation
        :param fan: type: User, the fan user
        :param star: type: User, the star user
        :return: result: type: Bool, the result whether the relation is existed
        """
        if fan is None or star is None:
            return False
        if not(isinstance(fan, User) and isinstance(star, User)):
            return False
        relation = Follow.objects.filter(star=star).filter(fan=fan)
        if len(relation) == 1:
            return True
        else:
            return False

    @classmethod
    def get_fans(cls, user):
        """
        get the fan of a user
        :param user: type: User, the user instance
        :return: result: type: Array, the result of fans
        """
        if user is None or not isinstance(user, User):
            return []
        relations = user.fan.all()
        return [relation.fan for relation in relations]

    @classmethod
    def get_stars(cls, user):
        """
        get the stars of a user
        :param user: type: User, the user instance
        :return: result: type: Array, the result of stars
        """
        if user is None or not isinstance(user, User):
            return []
        relations = user.star.all()
        return [relation.star for relation in relations]


class NotificationService(object):
    @classmethod
    def create_reply_notification(cls, instance):
        """
        Create a notification from the reply
        :param instance: type: Comment, the comment that creates notification
        :return: res: type: Notification, the created Notification
        """
        res = None
        # for comment post to a blog
        if instance.parent is None and instance.blog.author != instance.author:
            res = Notification.objects.create(type="Reply", content_object=instance, user=instance.blog.author)
        # else if comment post to another comment
        elif instance.parent is not None and instance.parent.author != instance.author:
            res = Notification.objects.create(type="Reply", content_object=instance, user=instance.parent.author)
        return res

    @classmethod
    def create_subscribe_notification(cls, instance):
        """
        Create a notification for users who subscribe the blog 'instance'
        :param instance: type: Blog, the blog that creates notification
        :return: res: type: list, list of the created Notifications
        """
        res = None
        # send notification to all followers
        author = instance.author
        relations = author.fan.all()
        fans = [relation.fan for relation in relations]
        res = []
        for fan in fans:
            notification = Notification.objects.create(type="Subscribe", content_object=instance, user=fan)
            res.append(notification)
        return res

    @classmethod
    def delete_notification(cls, instance):
        """
        Delete notifications related to instance
        :param instance: type: ???, the instance
        """
        ctype = ContentType.objects.get_for_model(instance)
        Notification.objects.filter(content_type=ctype).filter(object_id=instance.id).delete()

    @classmethod
    def create_at_notification(cls, instance, text):
        """
        check if the text has @ materials, then create the notification
        :param instance: type: ???, the instance
        :param text: type: str, the text of instance
        :return: res, type: list, the list of created notifications
        """
        name_list = re.findall('@([^\s]+)', text)
        res = []
        for name in name_list:
            user = User.objects.filter(username=name)
            if len(user) > 0:
                user = user[0]
                notification = Notification.objects.create(type="At", content_object=instance, user=user)
                res.append(notification)
        return res

    @classmethod
    def get_comment_reply_notifications(cls, user):
        """
        get comment_reply_notifications for user
        :param user: type: User, the user
        :return: res, type: list, the list of notifications
        """
        return user.notification_set.filter(type="Reply").filter(content_type__model='comment')

    @classmethod
    def get_unread_comment_reply_count(cls, user):
        """
        get the count of unread comments of specific user
        :param user: type: User, the user
        :return: res, type: int, the count
        """
        notifications = cls.get_comment_reply_notifications(user)
        res = notifications.filter(unread=True)
        return len(res)

    @classmethod
    def get_subscribe_blog_notifications(cls, user):
        """
        get the subscribe blog of the user
        :param user: type: User, the user
        :return: res, type: list, the list of notifications
        """
        return user.notification_set.filter(type="Subscribe").filter(content_type__model='blog')

    @classmethod
    def get_unread_subscribe_blog_count(cls, user):
        """
        get the count of unread subscribe blog
        :param user: type: User, the user
        :return: res, type: int, the count of notifications
        """
        notifications = cls.get_subscribe_blog_notifications(user)
        res = notifications.filter(unread=True)
        return len(res)

    @classmethod
    def get_at_blog_notifications(cls, user):
        """
        get the at notifications with type blog of the user
        :param user: type: User, the user
        :return: res, type: list, the list of notifications
        """
        return user.notification_set.filter(type="At").filter(content_type__model='blog')

    @classmethod
    def get_at_comment_notifications(cls, user):
        """
        get the at notifications with type comment of the user
        :param user: type: User, the user
        :return: res, type: list, the list of notifications
        """
        return user.notification_set.filter(type="At").filter(content_type__model='comment')

    @classmethod
    def get_unread_at_count(cls, user):
        """
        get the count of unread at notifications
        :param user: type: User, the user
        :return: res, type: int, the count of notifications
        """
        res = user.notification_set.filter(unread=True).filter(type="At")
        return len(res)

    @classmethod
    def get_unread_notification_count(cls, user):
        """
        get the count of unread notifications
        :param user: type: User, the user
        :return: res, type: int, the count of notifications
        """
        res = user.notification_set.filter(unread=True)
        return len(res)
