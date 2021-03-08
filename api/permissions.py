from rest_framework import permissions

class CanReadPlayer(permissions.BasePermission):

    def has_object_permission(self, request, view, player):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return False


class CanEditPlayer(permissions.BasePermission):
    
    def has_object_permission(self, request, view, player):

        # Requesting User must be connected to Player object for write access
        if request.method in ['PUT', 'PATCH']:
            try:
                if player.user == request.user:
                    return True

            # No user associated with player.
            except AttributeError:
                pass
        
        return False


class CanReadTeam(permissions.BasePermission):
    
    def has_object_permission(self, request, view, team):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True
        
        return False


class CanEditTeam(permissions.BasePermission):
    
    def has_object_permission(self, request, view, team):
        # Requesting User must be connected to Player object for write access
        if request.method in ['PUT', 'PATCH']:
            try:
                if (
                    team.captain.user == request.user and
                    team.circuit.season.is_active  
                ):
                    return True

            # No user associated with player.
            except AttributeError:
                pass
        
        return False
