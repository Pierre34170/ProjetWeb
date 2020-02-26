from django.shortcuts import render, redirect
from .forms import OrganizeForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

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

	return render(request, 'proposition/organize.html', context)


