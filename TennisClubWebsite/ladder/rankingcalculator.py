"""
Contains functions to compute ladder rankings
"""
from ladder.models import PlayerProfile, DoublesTeamProfile, Match
from django.db.models import Q
"""
Singles Scoring Systems
"""

def seven_point_system():
    matchlist = Match.objects.filter(matchtype='singles').reverse()
    players_all = PlayerProfile.objects.all()
    # Reset all player scores to their base scores
    # Note: Recalculating from entire history is not efficient but helps
    #       prevent scores from messing up when a match is deleted
    for player in players_all:
        player.matchstats.score = player.matchstats.basescore
        player.matchstats.numwon = 0
        player.matchstats.percentwon = 0
        player.matchstats.numplayed = 0
        player.matchstats.save()

    for match in matchlist:
        winner = match.winner1
        loser  = match.loser1
        
        if winner.matchstats.score >= loser.matchstats.score:
            # if winner is higher ranked, they get 7 points.
            winner.matchstats.score = winner.matchstats.score + 7
            
        elif winner.matchstats.score < loser.matchstats.score:
            # if winner is lower ranked, they get score of loser + 7 points. 
            winner.matchstats.score = loser.matchstats.score + 7

        # Loser always gets points = # of games won
        loser.matchstats.score  = loser.matchstats.score + match.loser_setscore

        # Update other matchstats
        winner.matchstats.numplayed += 1
        winner.matchstats.numwon += 1
        loser.matchstats.numplayed +=1

        # Save player data
        winner.matchstats.save()
        loser.matchstats.save()

    players = PlayerProfile.objects.filter(~Q(matchstats__numplayed=0))
    for player in players:
        player.matchstats.percentwon = round(100*player.matchstats.numwon/player.matchstats.numplayed)
        player.matchstats.save()   



""" 
Doubles Scoring System
"""

def update_matchstats_doubles_all():
    """
    recalculate stats for all teams
    """
    teams = DoublesTeamProfile.objects.all()
    matchlist = Match.objects.filter(matchtype='doubles')
    for team in teams:
        team.matchstats.numplayed = 0
        team.matchstats.numwon = 0
        team.matchstats.save()
    for match in matchlist:
        winningteam = DoublesTeamProfile.objects.get(player1 = match.winner1, player2 = match.winner2)
        losingteam = DoublesTeamProfile.objects.get(player1 = match.loser1, player2 = match.loser2)
        winningteam.matchstats.numplayed +=1
        winningteam.matchstats.numwon +=1
        losingteam.matchstats.numplayed +=1
        winningteam.matchstats.save()
        losingteam.matchstats.save()
        
    teams = DoublesTeamProfile.objects.filter(~Q(matchstats__numplayed=0))
    for team in teams:
        team.matchstats.percentwon = round(100*team.matchstats.numwon/team.matchstats.numplayed)
        team.matchstats.save()
    
