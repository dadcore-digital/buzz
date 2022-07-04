from django.db.models import Q

def can_create_team(circuit, user):
    """
    Can a requesting player create a Team in a given circuit?

    Current permissions logic:
        
        1. User must be signed in and have a player record
        
        2. Season linked to Circuit must have `registration_open` set to True

        3. User must not have already created a team in the requested Circuit

        4. Player can be a member of max two teams in a season, and their
           Region field must be set different. Tiers are not relevant.

            4a. UNLESS Region is set to "ALL", in which case we do not
                restrict number of teams created in this region.
    """
    from teams.models import Team  # Avoid circular import
    
    if user.is_anonymous:
        return False, 'Authentication Error: Sign in to create a team.'

    try:
        player = user.player

    except user._meta.model.player.RelatedObjectDoesNotExist:
        return False, 'Authentication Error: Your account does not have a Player associated with it.'

    if not circuit.season.registration_open:
        return False, 'Permission Error: Cannot create new team, registration for this season has closed.'

    elif circuit.season.registration_open:

        # Find all teams where requesting user is either captain or player
        existing_teams = Team.objects.filter(
            Q(circuit__season=circuit.season, captain=player) |
            Q(circuit__season=circuit.season, members__id=player.id)
        )

        # Exclude any team with region of "All" from the count of teams, see
        # rule 4a in docstring.
        existing_teams = existing_teams.exclude(circuit__region='A')

        # Only unique teams
        existing_teams = existing_teams.distinct()

        # Final number of unique teams captained, not in Region "ALL"
        num_teams = existing_teams.count()
        
        # We still limit you two create two teams per season (1 East, 1 West) 
        if num_teams >= 2:
            return False, 'Permission Error: You can only create two teams per season, one per region.'

        # You can only create one team per circuit
        elif num_teams == 1:            
            if existing_teams[0].circuit.region == circuit.region:
                return False, 'Permission Error: You have already registered a team for this circuit.'
        
        # Don't let captain create two teams in one Circuit, under any 
        # circumstance, even if Region is set to 'All'
        pre_existing_team_in_circuit = Team.objects.filter(
            Q(circuit=circuit, captain=player) |
            Q(circuit=circuit, members__id=player.id)
        ).exists()

        if pre_existing_team_in_circuit:
            return False, 'Permission Error: You have already registered a team for this circuit.'


    return True, None

def can_rename_team(team, user):
    """
    Return True if requester if ALL following permission checks are met:

    1. Requester is captain of team
    2. Season linked to team's circuit is active
    3. Season linked to team's circuit has registration_open set True    
    """
    from teams.models import Team
    
    if user.is_anonymous:
        return False, 'Authentication Error: Sign in to rename your team.'

    try:
        player = user.player

    except user._meta.model.player.RelatedObjectDoesNotExist:
        return False, 'Authentication Error: Your account does not have a Player associated with it.'
    
    if team.captain != player:
        return False, 'Permission Error: You must be the captain of this team to rename it.'
    
    elif not team.circuit.season.is_active:
        return False, 'Permission Error: Only teams in active seasons may be renamed.'

    elif not team.circuit.season.registration_open:
        return False, 'Permission Error: Only teams in seasons with open registration may be renamed.'

    return True, None

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

           4a. UNLESS this team is in a circuit of region "All" (A). We permit
               an unlimited number of teams in this region. However, player
               may only be in one team per circuit.
        
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

        # Special rules for "All" Region, see rule 4a in docstring
        if team.circuit.region == 'A':
            pre_existing_team_in_circuit = Team.objects.filter(
                Q(circuit=team.circuit, captain=player) |
                Q(circuit=team.circuit, members__id=player.id)
            ).exists()

            if pre_existing_team_in_circuit:
                return False
            
            return True

        # Apply normal rules restricting team membership to one per region
        else:
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

def can_regenerate_team_invite_code(team, user):
    """
    Return True if requesting user is team captain.
    """
    from teams.models import Team

    if user.is_anonymous:
        return False

    try:
        player = user.player

    except user._meta.model.player.RelatedObjectDoesNotExist:
        return False
    
    if team.captain == player:
        return True
        
    return False