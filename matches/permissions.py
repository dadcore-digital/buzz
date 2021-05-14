def can_create_match(user, return_error_msg=False):
    """
    Return True if requesting user can create a Match object.

    Normal users do not have this permission. Only users with permission of
    `matches.match.can_add_match` may create matches.

    By default all admin users have this permission.
    """
    has_perms = user.has_perm('matches.add_match')
    error_msg = 'Only service accounts can create matches.'

    if not has_perms:
        if return_error_msg:
            return False, error_msg
        else:
            return False

    else:
        if return_error_msg:
            return True, error_msg
        else:
            return True


def can_update_match(match, user):
    """
    Return True if requesting user can update a matche's start time or caster.

    Requester can set a Match.start_time if ALL conditions met:

    - User is authenticated
    - Requester is captain of Match.home or Match.away
    - Season associated with Match is active
    - NO Result object associated with Match
    """
    try:
        player = user.player

    except user._meta.model.player.RelatedObjectDoesNotExist:
        return False

    is_authenticated = user.is_authenticated
    is_captain = match.home.captain == player or match.away.captain == player
    season_is_active = match.circuit.season.is_active
    no_result = not hasattr(match, 'result')

    if all([is_authenticated, is_captain, season_is_active, no_result]):
        return True
        
    return False

def can_create_result(match, user, return_error_msg=False):
    """
    Return True if requesting user can create a Result object for a Match.

    Requester can create a Result object asocciated with a Match if ALL
    the following conditions are met:

    - User is authenticated
    - Requester is captain of Match.home or Match.away
    - Season associated with Match is active
    - NO Result object associated with Match
    
    Arguments:
    match -- Match to create Result object for. (obj)
    user -- User requesting to create Result object. (obj)
    error_message -- Return an descriptive error message along with boolean
                     result. (bool) (false)
    """
    try:
        player = user.player

    except user._meta.model.player.RelatedObjectDoesNotExist:
        if return_error_msg:
            return False, 'No Player object. You must be registered as a Player to submit a match result.'
        else:
            return False

    is_authenticated = user.is_authenticated
    is_captain = match.home.captain == player or match.away.captain == player
    season_is_active = match.circuit.season.is_active
    no_result = not hasattr(match, 'result')

    if all([is_authenticated, is_captain, season_is_active, no_result]):
        if return_error_msg:
            return True, None
        else:
            return True
    else:
        if not is_authenticated:
            error_msg = 'Permission Error: You must be signed in to submit a match result.'
        elif not is_captain:
            error_msg = 'Permission Error: Only team captains can submit match results.'
        elif not season_is_active:
            error_msg = 'Permission Error: You can only submit match results for active seasons.'
        elif not no_result:
            error_msg = 'Permission Error: There is already a result submitted for this match.'
        else:
            error_msg = 'Unknown Error :('

        if return_error_msg:
            return False, error_msg
        else:
            return False
