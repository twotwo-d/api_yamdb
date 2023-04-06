from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_superuser
        )


class IsAdminUserOrReadOnly(BasePermission):
    """Создадим разрешение для пользователей с правами администратора
    или только на чтение контента"""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin)


class IsAdminModeratorAuthorOrReadOnly(BasePermission):
    """Создадим разрешение для пользователей с правами администратора,
    модератора, автора или только на чтение контента"""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
