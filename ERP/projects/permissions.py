from rest_framework import permissions


class ManagerOrReadAndPatchOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
                request.method in ('GET', 'PATCH')
                or request.user.is_manager
            )


class ManagerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
                request.method == 'GET'
                or request.user.is_manager
            )
