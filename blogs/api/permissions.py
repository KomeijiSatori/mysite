from rest_framework.permissions import BasePermission


class IsOwnerOrSuperUser(BasePermission):
    message = "You must be the owner of this object."

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_superuser
