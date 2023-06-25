from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    message = 'Недостаточно прав'

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        """Общщеуровневое решение."""

        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and (
                request.user.is_admin
                or request.user.is_superuser
            )
        )


class IsAuthorOrAdminOrReadOnly(BasePermission):
    """Решение на уровне объектов. """
    message = 'Недостаточно прав'

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and (
                obj.author == request.user
                or request.user.is_admin
                or request.user.is_superuser)
        )


class IsAuthenticatedOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return True
