from django.forms import ModelForm, formset_factory
from .models import Match
from django_select2 import forms as s2forms
from leagues.models import Circuit, Round
from teams.models import Team

class CircuitWidget(s2forms.ModelSelect2Widget):

    def build_attrs(self, base_attrs, extra_attrs=None):
        """Add select2 data attributes."""
        default_attrs = {"data-minimum-input-length": 0}
        default_attrs["data-allow-clear"] = "false"

        default_attrs.update(base_attrs)
        attrs = super().build_attrs(default_attrs, extra_attrs=extra_attrs)

        if "class" in attrs:
            attrs["class"] += " django-select2"
        else:
            attrs["class"] = "django-select2"
        return attrs


    search_fields = [
        'name__icontains',
        'season__name__icontains',
        'season__league__name__icontains',
        'tier__icontains',
        'region__icontains'
    ]

class RoundWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        'name__icontains',
        'season__name__icontains',
        'round_number__iexact'
    ]

class TeamWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]

class MatchForm(ModelForm):

    class Meta:
        model = Match
        fields = ['circuit', 'round', 'home', 'away']

        widgets = {
            'home': TeamWidget,
            'away': TeamWidget,
            'circuit': CircuitWidget,
            'round': RoundWidget
        }

    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)

        self.fields['circuit'].queryset = Circuit.objects.filter(
            season__is_active=True 
        )
        self.fields['round'].queryset = Round.objects.filter(
            season__is_active=True 
        )
        self.fields['home'].queryset = Team.objects.filter(
            circuit__season__is_active=True 
        )        
        self.fields['away'].queryset = Team.objects.filter(
            circuit__season__is_active=True 
        )
    
MatchFormSet = formset_factory(MatchForm, extra=20)
