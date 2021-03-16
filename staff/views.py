from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.db.utils import IntegrityError
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from matches.forms import MatchForm, MatchFormSet
from matches.models import Match

@method_decorator(staff_member_required, name='dispatch')
class Home(TemplateView):
    template_name = 'staff/index.html'

@staff_member_required
def create_match(request):

    results = []

    if request.method == 'POST':
        formset = MatchFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                
                # Don't save empty extra forms
                if form.cleaned_data:
                    results.append(form.save())

            formset = MatchFormSet()    
    else:
        formset = MatchFormSet()
    return render(
        request, 'staff/match_form.html',
        {'matches_formset': formset, 'results': results})

# @method_decorator(staff_member_required, name='dispatch')
