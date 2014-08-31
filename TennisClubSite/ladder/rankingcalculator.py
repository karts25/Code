"""
Contains functions to compute ladder rankings
"""
from ladder.models import PlayerProfile, Match

"""
Singles Scoring Systems
"""

def seven_point_system():
    matchlist = Match.objects.all().filter(matchtype='singles').reverse()
    players_all = PlayerProfile.objects.all()
    
    # Reset all player scores to their base scores
    # Note: Recalculating from entire history is not efficient but helps
    #       prevent scores from messing up when a match is deleted
    for player in players_all:
        player.score = player.basescore
        print player.score
        player.save()

    for match in matchlist:
        player1_name = match.team1_id1
        player2_name = match.team2_id1
        player1 = players_all.get(user__username__exact=player1_name)
        player2 = players_all.get(user__username__exact=player2_name)
        
        if match.team1_setscore > match.team2_setscore:
            losingscore = match.team2_setscore
        else:
            losingscore = match.team1_setscore

        # find higher ranked player
        if player1.score > player2.score:
            higher_ranked = player1
            lower_ranked  = player2
        else:
            higher_ranked = player2
            lower_ranked = player1
            
        if match.isWinner(higher_ranked):
            # if winner is higher_ranked ranked, they get 7 points
            higher_ranked.score = higher_ranked.score + 7
            # loser gets 1 point for each game they win
            lower_ranked.score = lower_ranked.score + losingscore
        else:
            # if winner is lower_ranked ranked, their score is now score of higher_ranked ranked + 7
            lower_ranked.score = higher_ranked.score+7
            # loser gets 1 point for each game they win
            higher_ranked.score = higher_ranked.score + losingscore
            
        # Save player data
        higher_ranked.save()
        lower_ranked.save()

def winpercent_singles():
    players_all = PlayerProfile.objects.all()
    for player in players_all:
        player.singles_winpercent = calculate_winpercent(player,'singles')
        player.save()

def calculate_winpercent(player,match_type):
    matchlist = player.matches.filter(matchtype=match_type)
    wins = 0
    for match in matchlist:
        if match.isWinner(player):
            wins +=1
    winningpercent = wins/matchlist.count()
    return winningpercent

