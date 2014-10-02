from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse
from ladder.models import PlayerProfile,Match,DoublesTeamProfile,MatchStats
from django.template import RequestContext, loader
from ladder.recordform import RecordForm
from django.core.exceptions import ValidationError
import rankingcalculator

def roster(request):
    template = loader.get_template('ladder/roster.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def record(request,err=''):
    playerlist = PlayerProfile.objects.all()
    template = loader.get_template('ladder/record.html')
    context = RequestContext(request,{
            'playerlist':playerlist,
            'error':err,
            })
    return HttpResponse(template.render(context))

    #return render(request,'ladder/record.html')


def history(request,msg=''):
    matchlist = Match.objects.all()
    template = loader.get_template('ladder/history.html')
    context = RequestContext(request,{
            'matchlist':matchlist,
            'msg':msg,
            })
    return HttpResponse(template.render(context))


def recorded(request):
    # TODO: Proper form validation. Currently very hacky
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    
    if user is None:
        return record(request,'*** ERROR: User login information is not valid')

    form = RecordForm(request.POST)
    if not form.is_valid():
        return record(request,'*** ERROR: Please check if Match Type, Date and scores are valid')
    matchtype = request.POST['matchtype']
    matchdate = request.POST['matchdate']
    team1_id1 = request.POST['team1id1']
    team1_player1 = PlayerProfile.objects.get(user__username__exact = team1_id1)
    team2_id1 = request.POST['team2id1']
    team2_player1 = PlayerProfile.objects.get(user__username__exact = team2_id1)
    team1_setscore = request.POST['team1_setscore']
    team2_setscore = request.POST['team2_setscore']
    team1_id2 = request.POST['team1id2']
    team2_id2 = request.POST['team2id2']
    
    #if (team1_setscore !=6) and (team2_setscore !=6):
    #    print team1_setscore, team2_setscore, (team1_setscore!=6)
#return record(request,'*** ERROR! The winner has to have 6 games.')

    if (team1_id1 == team2_id1):
        return record(request,'*** ERROR: Same player on both sides of the net!')

    if team1_setscore > team2_setscore:
        winner1 = team1_player1
        winner_setscore = team1_setscore
        loser1 = team2_player1
        loser_setscore = team2_setscore
    else:
        winner1 = team2_player1
        winner_setscore = team2_setscore
        loser1 = team1_player1
        loser_setscore = team1_setscore

    # Add new match to the list of matches
    if matchtype=='singles':            
        if team1_id2 or team2_id2:
            return record(request,'*** ERROR: Two team members entered for a singles match.')
        if winner1.gender != loser1.gender:
            return record(request,'*** ERROR: Mixed gender singles matches are not recorded in the ladder')

        match = Match(matchtype=matchtype,matchdate=matchdate,
                      winner1 = winner1, loser1 = loser1, 
                      winner_setscore=winner_setscore,loser_setscore=loser_setscore)
        match.save()
        rankingcalculator.seven_point_system()
    else:
        if (not team1_id2) or (not team2_id2):
            return record(request,'*** ERROR: Player 2 required for doubles')
        
        if len(set([team1_id1,team1_id2,team2_id1,team2_id2])) < 4:
            return record(request,'*** ERROR: All 4 players must be unique')
            
        team1_player2 = PlayerProfile.objects.get(user__username__exact = team1_id2)
        team2_player2 = PlayerProfile.objects.get(user__username__exact = team2_id2)

        # Sort alphabetically
        if team1_id2 < team1_id1:
            temp = team1_player1
            team1_player1 = team1_player2
            team1_player2 = temp
        if team2_id2 < team2_id1:
            temp = team2_player1
            team2_player1 = team2_player2
            team2_player2 = temp
        
        # if team1 is new, make a profile for them    
        doublesteamprofile1 = DoublesTeamProfile.objects.filter(player1 = team1_player1, 
                                                             player2 = team1_player2)
        if not doublesteamprofile1:
            if team1_player1.gender == 'M' and team1_player2.gender == 'M':
                gender = 'M'
            elif team1_player1.gender == 'W' and team1_player2.gender == 'W':
                gender = 'W'
            else:
                gender = 'X'
            matchstats1 = MatchStats()
            matchstats1.save()
          
            doublesteamprofile1 = DoublesTeamProfile(player1=team1_player1,
                                                     player2=team1_player2,
                                                     gender=gender,matchstats=matchstats1)
            doublesteamprofile1.save()

        else:
            doublesteamprofile1 = DoublesTeamProfile.objects.get(player1 = team1_player1, 
                                                                 player2 = team1_player2)

        # if team2 is new, make a profile for them    
        doublesteamprofile2 = DoublesTeamProfile.objects.filter(player1 = team2_player1, 
                                                             player2 = team2_player2)
        if not doublesteamprofile2:
            if team2_player1.gender == 'M' and team2_player2.gender == 'M':
                gender = 'M'
            elif team2_player1.gender == 'W' and team2_player2.gender == 'W':
                gender = 'W'
            else:
                gender = 'X'
            matchstats2 = MatchStats()
            matchstats2.save()
            doublesteamprofile2 = DoublesTeamProfile(player1=team2_player1,
                                                     player2=team2_player2,
                                                     gender=gender,matchstats=matchstats2)  
            doublesteamprofile2.save()
        else:
            doublesteamprofile2 = DoublesTeamProfile.objects.get(player1 = team2_player1, 
                                                                    player2 = team2_player2)

        # Create match object for this match
        if team1_setscore > team2_setscore:
            winner1 = team1_player1
            winner2 = team1_player2
            loser1  = team2_player1
            loser2  = team2_player2
        else:
            winner1 = team2_player1
            winner2 = team2_player2
            loser1  = team1_player1
            loser2  = team1_player2
        match = Match(matchtype=matchtype,matchdate=request.POST['matchdate'],
                      winner1 = winner1, winner2 = winner2, loser1 = loser1, loser2 = loser2,
                      winner_setscore=winner_setscore,loser_setscore=loser_setscore)        
        match.save()
        rankingcalculator.update_matchstats_doubles_all()

    return redirect('/ladder/history',request,'Match successfully recorded!')
    
def rankings_singles(request):
    # Update player scores
    playerlist_men = PlayerProfile.objects.filter(gender='M').order_by('-matchstats__score','-matchstats__percentwon','-matchstats__numplayed')
    playerlist_women = PlayerProfile.objects.filter(gender='W').order_by('-matchstats__score','-matchstats__percentwon','-matchstats__numplayed')
    template = loader.get_template('ladder/singles.html')
    context = RequestContext(request,{
            'playerlist_men':playerlist_men,
            'playerlist_women':playerlist_women,
            })
    return HttpResponse(template.render(context))
        

def rankings_doubles(request):
    teamlist_men = DoublesTeamProfile.objects.filter(gender='M').order_by('-matchstats__percentwon','-matchstats__numplayed')
    teamlist_women = DoublesTeamProfile.objects.filter(gender='W').order_by('-matchstats__percentwon','-matchstats__numplayed')
    teamlist_mixed = DoublesTeamProfile.objects.filter(gender='X').order_by('-matchstats__percentwon','-matchstats__numplayed')
    template = loader.get_template('ladder/doubles.html')
    context = RequestContext(request,{
            'teamlist_men':teamlist_men,
            'teamlist_women':teamlist_women,
            'teamlist_mixed':teamlist_mixed,
            })
    return HttpResponse(template.render(context))

