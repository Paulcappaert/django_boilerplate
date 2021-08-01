from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if view.action in ('create',):
            return True

        if view.action in ('retrieve', 'update', 'partial_update', 'destroy'):
            if request.user.is_authenticated and request.user == obj:
                return True

        return False
