from django import forms
from .models import User
from choice.models import dish

choices = []
for i in dish.objects.all():
    choices += [(i.ref, str(i.ref))]

CHOICES = tuple(choices)

class choice_form(forms.Form):
    choose = forms.ChoiceField(
        required=False,
        choices=CHOICES,
        )
    
