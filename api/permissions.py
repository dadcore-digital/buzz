from rest_framework import permissions
from matches.permissions import (
    can_create_match, can_create_result, can_update_match)
from matches.models import Match
from teams.permissions import can_create_team, can_rename_team

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
    
    message = 'Cannot rename team'

    def has_object_permission(self, request, view, team):
        # Requesting User must be connected to Player object for write access
        if request.method in ['PUT', 'PATCH']:
            has_permission, error = can_rename_team(team, request.user)
            
            if has_permission:
                return True
            else:
                self.message = error

        return False


class CanCreateMatch(permissions.BasePermission):
        
    def has_permission(self, request, view):
        import ipdb; ipdb.set_trace() 
        
        if request.method in ['POST']:
            return can_create_match(request.user)

        return False

class CanReadMatch(permissions.BasePermission):
    
    def has_object_permission(self, request, view, team):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return False

class CanUpdateMatch(permissions.BasePermission):
    
    def has_object_permission(self, request, view, match):
        if request.method in ['PATCH']:
            return can_update_match(match, request.user)

        return False

class CanReadResult(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, team):
        return request.method in permissions.SAFE_METHODS


class CanCreateResult(permissions.BasePermission):
        
    def has_permission(self, request, view):
        if request.method in ['POST']:
            return True
