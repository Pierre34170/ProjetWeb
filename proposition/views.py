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
from .models import Proposition, Training, Match
from account.models import Team
from .forms import ResearchMatchForm
from django.contrib.auth.decorators import user_passes_test

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

class PropositionListView(LoginRequiredMixin, ListView):
	model = Proposition
#	temmplate_name = 'proposition/display_games.html'
	context_object_name = 'propositions'
	ordering = ['-date_posted']



'''	def display_propositions(self):
		propositions=Proposition.objects.get(date_match > timezone.now)
'''

class PropositionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
	model = Proposition

	def test_func(self):
		if self.request.user.is_captain:
			return True
		return False


class PropositionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Proposition
	fields = ['title', 'date_match', 'match']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		if self.request.user.is_captain:
			return True
		return False

class PropositionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Proposition
	fields = ['title', 'date_match', 'match']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		proposition = self.get_object()
		if (self.request.user.is_captain and self.request.user == proposition.author):
			return True
		return False


class PropositionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Proposition
	success_url = '/'

	def test_func(self):
		proposition = self.get_object()
		if (self.request.user.is_captain and self.request.user == proposition.author):
			return True
		return False



''' Gestion des entrainements '''


class TrainingListView(ListView):
	model = Training
	context_object_name = 'trainings'
	ordering = ['-date_posted']


class TrainingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
	model = Training

	def test_func(self):
		if self.request.user.is_captain:
			return True
		return False

class TrainingCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Training
	fields = ['date_training', 'hour_training', 'type_training', 'team_training']

	def form_valid(self, form):
		form.instance.team_training = self.request.user.team
		return super().form_valid(form)

	def test_func(self):
		if self.request.user.is_captain:
			return True
		return False


class TrainingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Training
	fields = ['date_training', 'hour_training', 'type_training', 'team_training']

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

class TeamCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Team
	fields = ['libelle_team']

	def form_valid(self, form):
		self.request.user.team = form.instance
		return super().form_valid(form)


	def test_func(self):
		if self.request.user.is_captain:
			return True
		return False

# creer son match avant de le proposer 

class MatchCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Match
	fields = ['real_date', 'hour_beggin', 'lieu_match']

	def form_valid(self, form):

		return super().form_valid(form)

	def test_func(self):
		if self.request.user.is_captain:
			return True
		return False



# rechercher une proposition de matchs a une date donnée

def is_captain_check(user):
	return user.is_captain


@login_required
@user_passes_test(is_captain_check, login_url='home')
def ResearchMatch(request):
	if request.method=='POST':
		form = ResearchMatchForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			date = instance.date_match
			propositions = Proposition.objects.filter(date_match= date)
			context = {'form' : form, 'propositions' : propositions}
			return render(request, 'proposition/proposition_list.html', context)
	else:
		form = ResearchMatchForm()

	context = {'form' : form}

	return render(request, 'proposition/proposition_list.html', context)




