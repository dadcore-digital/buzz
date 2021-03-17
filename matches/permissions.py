def can_update_match_time(match, user):
    """
    Return True if requesting user can update a matche's start time.

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
