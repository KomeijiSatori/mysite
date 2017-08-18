from django.contrib.auth.models import User

from .models import Follow


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
