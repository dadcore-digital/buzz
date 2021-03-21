from rest_framework import permissions
from matches.permissions import can_create_result, can_update_match_time
from matches.models import Match
from teams.permissions import can_create_team

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


class CanUpdateTeam(permissions.BasePermission):
    
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


class CanReadMatch(permissions.BasePermission):
    
    def has_object_permission(self, request, view, team):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return False

class CanUpdateMatchTime(permissions.BasePermission):
    
    def has_object_permission(self, request, view, match):
        if request.method in ['PATCH']:
            return can_update_match_time(match, request.user)

        return False

class CanReadResult(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, team):
        return request.method in permissions.SAFE_METHODS


class CanCreateResult(permissions.BasePermission):
        
    def has_permission(self, request, view):
        if request.method in ['POST']:
            match = Match.objects.filter(id=request.data['match']).first()
            
            # Can't submit results for a bogus Match
            if not match:
                return False

            return can_create_result(match, request.user)

