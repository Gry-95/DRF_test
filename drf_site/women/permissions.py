from rest_framework import permissions


class IsAdminReadOnly(permissions.BasePermission):
    def has_permission(self, request,
                       view):  # Переопределяем метод родительского класса, что бы настроить чтение для всех, удаление - админ
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
