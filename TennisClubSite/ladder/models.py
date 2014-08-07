from django.db import models
from django.contrib.auth.models import User
from ast import literal_eval
    

class Match(models.Model):    
    matchtype   = models.CharField(max_length=200)
    matchdate   = models.DateField()
    
    team1_setscore   = models.IntegerField(default=0)
    team2_setscore   = models.IntegerField(default=0)     
    team1_id1        = models.CharField(max_length=200)
    team1_id2        = models.CharField(max_length=200)
    team2_id1        = models.CharField(max_length=200)
    team2_id2        = models.CharField(max_length=200)
    class Meta:
        ordering = ('-matchdate',)

    def isWinner(self,player):
        """
        Given a player, check if he/she won the match
        """
        playername = player.user.username
        #team1 = [self.team1_id1 self.team1_id2]
        #team2 = [self.team2_id1 self.team2_id2]
    
        if playername == self.team1_id1 or playername == self.team1_id2:
            if self.team1_setscore >= self.team2_setscore:
                return True
            else:
                return False
        elif playername == self.team2_id1 or playername == self.team2_id2:
            if self.team2_setscore >= self.team1_setscore:
                return True
            else:
                return False
        else: # player not involved in match
            return False


class PlayerProfile(models.Model):
    user      = models.OneToOneField(User)
    
    MALE      = 'M'
    FEMALE    = 'W'
    GENDER_CHOICES = ((MALE,'Male'),(FEMALE,'Female'))
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default=MALE) 

    basescore = models.IntegerField(default=0) # added to ladder rank
    matches   = models.ManyToManyField(Match,blank='true')
    

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
    
    
                                         
