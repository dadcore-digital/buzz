from django.db import models
from django.db.models import Count, Case, When, F, IntegerField
from django.db.models.functions import Coalesce

class ResultManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().annotate(
            sets_total=Coalesce(models.Count('sets'), 0)
        ).annotate(sets_home=Count(
                Case(
                    When(sets__winner=F('match__home'), then=1),
                    output_field=IntegerField()
                )
            )
        ).annotate(sets_away=Count(
                Case(
                    When(sets__winner=F('match__away'), then=1),
                    output_field=IntegerField()
                )
            )
        )

class SetManager(models.Manager):

    def won_away(self):
        qs = self.get_queryset()
        return qs.filter(winner=F('result__match__away'))

    def won_home(self):
        qs = self.get_queryset()
        return qs.filter(winner=F('result__match__home'))
