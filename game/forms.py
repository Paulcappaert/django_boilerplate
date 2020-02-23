from django import forms
from django.shortcuts import get_object_or_404
from .models import Game
from core.models import User

class GameForm(forms.Form):
    opponent = forms.ModelChoiceField(User.objects.all())
    color = forms.ChoiceField(choices=(('w', 'white'),('b', 'black')), label='your color')

    def start_game(self, user):
        other = self.cleaned_data['opponent']
        color = self.cleaned_data['color']
        if color == 'w':
            game = Game.objects.create(p1=user, p2=other)
        elif color == 'b':
            game = Game.objects.create(p1=other, p2=user)
        return game
    