from django import forms
from ladder.models import PlayerProfile
from django.core import validators

CHOICES_MATCHTYPE=[('singles', 'Singles'),
         ('doubles', 'Doubles')]
class RecordForm(forms.Form):
    matchtype = forms.ChoiceField(choices=CHOICES_MATCHTYPE,widget=forms.RadioSelect())
    matchdate = forms.DateField()
    team1_setscore = forms.IntegerField(max_value=6, min_value=0)
    team2_setscore = forms.IntegerField(max_value=6, min_value=0)

    
