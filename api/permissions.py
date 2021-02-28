from rest_framework import permissions

class CanAccessPlayer(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Requesting User must be connected to Player object for write access
        if request.method == 'PUT':
            try:
                if obj.user == request.user:
                    return True

            # No user associated with player.
            except AttributeError:
                pass
        
        return False
