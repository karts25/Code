from django.db import models
from django.contrib.auth.models import User
from ast import literal_eval
    

class MatchStats(models.Model):
    """
    Stores match statistics that are displayed on ladder webpage. Each PlayerProfile as well as each Team has a reference to one such objects
    """
    basescore          = models.IntegerField(default=0)
    score              = models.IntegerField(default=0)
    
    numplayed          = models.IntegerField(default=0)
    numwon             = models.IntegerField(default=0)
    percentwon         = models.IntegerField(default=0)
         

class PlayerProfile(models.Model):
    user      = models.OneToOneField(User)    
    MALE      = 'M'
    FEMALE    = 'W'
    GENDER_CHOICES = ((MALE,'Male'),(FEMALE,'Female'))
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default=MALE) 
    #matches   = models.ManyToManyField(Match,blank='true')
    matchstats = models.OneToOneField(MatchStats)
    
    def __unicode__(self):
        return self.user.username
    #Additional User Attributes

    def score_from_matchlist(self,matchlist):
        """
        Given list of matches, calculate total score.
        Score is calculated as:
        +1 for every match played
        An additional +2 for every match won
        """
        score = self.basescore + len(matchlist)
        for match in matchlist:
            if match.isWinner(self):
                score += 1
        return score
                        
    def score_all(self):
        return self.score_from_matchlist(self.matches.all())

    def score_singles(self):
        return self.score_from_matchlist(self.matches.get(matchtype__exact="singles"))
    
    
class DoublesTeamProfile(models.Model):
    """
    Always enter the team such that player1 is alphabetically before player 2
    """
    player1  = models.ForeignKey(PlayerProfile, related_name='player1')
    player2  = models.ForeignKey(PlayerProfile, related_name='player2')
    MALE     = 'M'
    FEMALE   = 'W'
    MIXED    = 'X'
    GENDER_CHOICES = ((MALE,'Male'),(FEMALE,'Female'),(MIXED,'Mixed'))
    gender   = models.CharField(max_length=1,choices=GENDER_CHOICES,default=MALE)
    matchstats = models.OneToOneField(MatchStats)
                        
class Match(models.Model):    
    matchtype   = models.CharField(max_length=200)
    matchdate   = models.DateField()
    
    winner_setscore   = models.IntegerField(default=0)
    loser_setscore   = models.IntegerField(default=0)     
    #winner_id1        = models.CharField(max_length=200)
    #winner_id2        = models.CharField(max_length=200)
    #loser_id1        = models.CharField(max_length=200)
    #loser_id2        = models.CharField(max_length=200)
    winner1           = models.ForeignKey(PlayerProfile,related_name='winner1')
    winner2           = models.ForeignKey(PlayerProfile,related_name='winner2',null=True)
    loser1            = models.ForeignKey(PlayerProfile,related_name='loser1')
    loser2            = models.ForeignKey(PlayerProfile,related_name='loser2',null=True)
    class Meta:
        ordering = ('-matchdate',)
    
