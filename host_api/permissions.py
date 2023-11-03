from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        """
        Checks if the user has permission to perform a certain action.

        Parameters:
            - request: The HTTP request object.
            - view: The view object.

        Returns:
            - bool: True if the user has permission, False otherwise.
        """
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated
            )
            or (request.user and request.user.is_staff)
        )


class IsOwnerOrAdminOrReadOnly(BasePermission):
    """
    Check if the user has permission to access the specified object.

    Args:
        request (HttpRequest): The request object.
        view (View): The view that is being accessed.
        obj (Object): The object that is being accessed.

    Returns:
        bool: True if the user has permission, False otherwise.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user or request.user.is_staff
