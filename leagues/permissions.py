from django.db.models import Q

def can_create_team(circuit, player):
    """
    Can a requesting player create a Team in a given circuit?

    Current permissions logic:
        
        1. Season linked to Circuit must have `registration_open` set to True
        
        2. Player can be a member of max two teams in a season, and their
           Region field must be set different. Tiers are not relevant.
    """
    from teams.models import Team  # Avoid circular import
    
    
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
