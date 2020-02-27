from django.shortcuts import render, redirect
from .forms import OrganizeForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView

from .models import Proposition


@login_required

def organize_view(request):

	form = OrganizeForm()
	if request.method == 'POST':
		print('Printing POST:', request.POST)
		form = OrganizeForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'proposition/organize.html', context)



@login_required

def display_games_view(request):
	context = {
		'propositions': Proposition.objects.all()
	}

	return render(request, 'proposition/proposition_list.html', context)



class PropositionListView(ListView):
	model = Proposition
#	temmplate_name = 'proposition/display_games.html'
	context_object_name = 'propositions'
	ordering = ['-date_posted']

class PropositionDetailView(DetailView):
	model = Proposition