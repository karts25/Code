from django import forms
from ladder.models import PlayerProfile
from django.core import validators

CHOICES_MATCHTYPE=[('singles', 'Singles'),
         ('doubles', 'Doubles')]
class RecordForm(forms.Form):
    matchtype = forms.ChoiceField(choices=CHOICES_MATCHTYPE,widget=forms.RadioSelect())
    matchdate = forms.DateField()
    #print [(o.user.username, o.user.username) for o in PlayerProfile.objects.all()]
    team1_id1 = forms.ChoiceField(choices=[(o.user.username, o.user.username) for o in PlayerProfile.objects.all()],
                                  required=False)
    team1_id2 = forms.ChoiceField(choices=[(o.user.username, o.user.username) for o in PlayerProfile.objects.all()]+[('','None')],
                                  required=False)
    team2_id1 = forms.ChoiceField(choices=[(o.user.username, o.user.username) for o in PlayerProfile.objects.all()],
                                  required=False)
    team2_id2 = forms.ChoiceField(choices=[(o.user.username, o.user.username) for o in PlayerProfile.objects.all()] + [('','None')])
    team1_setscore = forms.IntegerField(max_value=6, min_value=0)
    team2_setscore = forms.IntegerField(max_value=6, min_value=0)

    def clean_doublesplayers(self):
        print "team1_id2"
        team1_id2 = self.cleaned_data['team1_id2']
        team2_id2 = self.cleaned_data['team2_id2']
        print "team1_id2",team1_id2,team2_id2
        if (team1_id2 == '') or (team2_id2 == ''):
            raise forms.ValidationError("Need to enter teammate's names")
        
