from django.db.models import Q

def can_create_team(circuit, user):
    """
    Can a requesting player create a Team in a given circuit?

    Current permissions logic:
        
        1. User must be signed in and have a player record
        
        2. Season linked to Circuit must have `registration_open` set to True
        
        3. Player can be a member of max two teams in a season, and their
           Region field must be set different. Tiers are not relevant.
    """
    from teams.models import Team  # Avoid circular import
    
    if user.is_anonymous:
        return False

    try:
        player = user.player

    except user._meta.model.player.RelatedObjectDoesNotExist:
        return False

    if circuit.season.registration_open:

        existing_teams = Team.objects.filter(
            Q(circuit__season=circuit.season, captain=player) |
            Q(circuit__season=circuit.season, members__id=player.id)
        ).distinct()

        num_teams = existing_teams.count()
        
        if num_teams == 0:            
            return True
        
        elif num_teams == 1:
            if existing_teams[0].circuit.region != circuit.region:
                return True

    return False

def can_join_team(team, user, invite_code):
    """
    Can a requesting player join a Team?

    Current permissions logic:
        
        1. User must be signed in and have a player record.

        2. Player must pass a valid invite code for this team

        3. Team.can_add_members() must return True, currently this means:
           
           - Season associated with team has `rosters_open=True`
           - Team member count < seaon's `max_team_members`
        
        4. Player can be a member of max two teams in a season, and their
           Region field must be set different. Tiers are not relevant.
        
        5. Player cannot already be a member of this team 
    """
    from teams.models import Team

    if user.is_anonymous:
        return False

    try:
        player = user.player

    except user._meta.model.player.RelatedObjectDoesNotExist:
        return False
    
    valid_invite = invite_code == team.invite_code
    is_existing_member = team.members.filter(id=player.id)
    
    if (
        valid_invite and 
        team.can_add_members and not
        is_existing_member
    ):
        existing_teams = Team.objects.filter(
            Q(circuit__season=team.circuit.season, captain=player) |
            Q(circuit__season=team.circuit.season, members__id=player.id)
        ).distinct()

        num_teams = existing_teams.count()
        
        if num_teams == 0:            
            return True
        
        elif num_teams == 1:
            if existing_teams[0].circuit.region != team.circuit.region:
                return True

    return False
