from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from ladder.models import PlayerProfile,Match
from django.template import RequestContext, loader
import rankingcalculator

def record(request):
    playerlist = PlayerProfile.objects.all()
    template = loader.get_template('ladder/record.html')
    context = RequestContext(request,{
            'playerlist':playerlist,
            })
    return HttpResponse(template.render(context))

    #return render(request,'ladder/record.html')

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
    
    # Update player scores
    rankingcalculator.seven_point_system()
    return(history(request))
    

def history(request):
    matchlist = Match.objects.all()
    template = loader.get_template('ladder/history.html')
    context = RequestContext(request,{
            'matchlist':matchlist,
            })
    return HttpResponse(template.render(context))


def rankings_singles(request):
    # Update player scores
    # TODO: Make this a daily event
    rankingcalculator.seven_point_system()

    playerlist_men = PlayerProfile.objects.filter(gender='M').order_by('-score')
    playerlist_women = PlayerProfile.objects.filter(gender='W').order_by('-score')
    template = loader.get_template('ladder/singles.html')
    context = RequestContext(request,{
            'playerlist_men':playerlist_men,
            'playerlist_women':playerlist_women,
            })
    return HttpResponse(template.render(context))
        
"""
def index(request):
    template = loader.get_template('ladder/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def about(request):
    template = loader.get_template('ladder/about.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
"""
