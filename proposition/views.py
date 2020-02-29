from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import OrganizeForm
from django.contrib.auth.decorators import login_required
from django.views.generic import (
	ListView, 
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
	)

from django.utils import timezone
from .models import Proposition, Training
from account.models import Team
from .forms import FindMatchForm

'''
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
'''




''' gestion des propositions de matchs  '''

class PropositionListView(ListView):
	model = Proposition
#	temmplate_name = 'proposition/display_games.html'
	context_object_name = 'propositions'
	ordering = ['-date_posted']

'''	def display_propositions(self):
		propositions=Proposition.objects.get(date_match > timezone.now)
'''

class PropositionDetailView(DetailView):
	model = Proposition



class PropositionCreateView(LoginRequiredMixin, CreateView):
	model = Proposition
	fields = ['title', 'date_match', 'match']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PropositionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Proposition
	fields = ['title', 'date_match', 'match']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		proposition = self.get_object()
		if self.request.user == proposition.author:
			return True
		return False

class PropositionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Proposition
	success_url = '/'

	def test_func(self):
		proposition = self.get_object()
		if self.request.user == proposition.author:
			return True
		return False





''' Gestion des entrainements '''


class TrainingListView(ListView):
	model = Training
	context_object_name = 'trainings'
	ordering = ['-date_posted']



class TrainingDetailView(DetailView):
	model = Training



class TrainingCreateView(LoginRequiredMixin, CreateView):
	model = Training
	fields = ['title_training', 'date_training', 'type_training', 'team_training']

	def form_valid(self, form):
		form.instance.team_training = self.request.user.team
		return super().form_valid(form)



class TrainingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Training
	fields = ['title_training', 'date_training', 'type_training', 'team_training']

	def form_valid(self, form):
		form.instance.team_training = self.request.user.team
		return super().form_valid(form)

	def test_func(self):
		training = self.get_object()
		if (self.request.user.team == training.team_training and self.request.user.is_captain):
			return True
		return False

class TrainingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Training
	success_url = '/'

	def test_func(self):
		training = self.get_object()
		if (self.request.user.team == training.team_training and self.request.user.is_captain):
			return True
		return False




''' Creer son equipe '''

class TeamCreateView(LoginRequiredMixin, CreateView):
	model = Team
	fields = ['libelle_team']

	def form_valid(self, form):
		self.request.user.team = form.instance
		return super().form_valid(form)


def FindMatch(request):
	if request.method=='POST':
		form = FindMatchForm(request.POST)
		if form.is_valid():
			instance = form.save()
			date = instance.date_match
			propositions = Proposition.objects.get(date_match = date)
			context = {'form' : form, 'proposition' : proposition}
			return render(request, 'proposition/proposition_list.html', context)


	else:
		form = FindMatchForm()

	context = {'form' : form}

	return render(request, 'proposition/proposition_list.html', context)



