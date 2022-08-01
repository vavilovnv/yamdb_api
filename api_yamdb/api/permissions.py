from rest_framework import permissions

ROLE_USER = 'user'
ROLE_ADMIN = 'admin'
ROLE_MODERATOR = 'moderator'


class AdminPermission(permissions.BasePermission):
    """Права доступа администратора."""

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if (request.user.is_authenticated
                and request.user.role == ROLE_ADMIN):
            return True


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Права доступа к записям: автору записи всё, остальным чтение."""
    message = 'Разрешено изменять только собственные записи!'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
