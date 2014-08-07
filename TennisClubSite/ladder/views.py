from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from ladder.models import PlayerProfile,Match
from django.template import RequestContext, loader

def record(request):
    return render(request,'ladder/record.html')

def recorded(request):
    # TODO: Sanitize inputs
    
    # Add new match to the list of matches
    match = Match(matchtype=request.POST['matchtype'],matchdate=request.POST['matchdate'],
                  team1_id1=request.POST['team1id1'], team1_id2 = request.POST['team1id2'],
                  team2_id1=request.POST['team2id1'], team2_id2 = request.POST['team2id2'],
                  team1_setscore=request.POST['team1_setscore'],team2_setscore=request.POST['team2_setscore'])
    match.save()
    # Register match to players
    players_all = PlayerProfile.objects
    if match.matchtype=='singles':
        player_names = [request.POST['team1id1'],request.POST['team2id1']]
    else:
        player_names = [request.POST['team1id1'],request.POST['team2id1'],request.POST['team1id2'],request.POST['team2id2']]
    
    for player_name in player_names:
        player = players_all.get(user__username__exact=player_name)
        player.matches.add(match)
        player.save
    
    return(history(request))
    

def history(request):
    matchlist = Match.objects.all()
    template = loader.get_template('ladder/history.html')
    context = RequestContext(request,{
            'matchlist':matchlist,
            })
    return HttpResponse(template.render(context))

def rankings(request):
    players_all = PlayerProfile.objects.all()
    for player in players_all:
        score = player.score_all()
        print player.user.username,score
    return HttpResponse(score)
        
