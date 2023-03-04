from rest_framework import permissions


class ManagerOrReadAndPatchOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated and (
            request.method in ('GET', 'PATCH') or
            request.user.is_manager or
            request.user.is_admin
                ))

    def has_object_permission(self, request, view, obj):
        return (
            obj.project.manager == request.user or
            request.user.is_admin or
            (request.user.is_executer and request.method in ('GET', 'PATCH'))
            )


class ManagerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated and (
            request.method == 'GET' or
            request.user.is_manager or
            request.user.is_admin
                ))

    def has_object_permission(self, request, view, obj):
        return obj.manager == request.user or request.user.is_admin


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class ManagerOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_manager
        )


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.method == 'GET'
            )
