from rest_framework import permissions


class ManagerOrReadAndPatchOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated and (
            request.method in ('GET', 'PATCH') or
            request.user.is_manager or
            request.user.is_admin
                ))


class ManagerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated and (
            request.method == 'GET' or
            request.user.is_manager or
            request.user.is_admin
                ))


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class ManagerOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_manager
        )
