from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
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

from django.contrib import messages

from django.utils import timezone
from .models import Proposition, Training, Reserve
from account.models import Team, Account
from .forms import ResearchMatchForm, SuggestTrainingForm
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
	ordering = ['date_posted']



'''	def display_propositions(self):
		propositions=Proposition.objects.get(date_match > timezone.now)
'''

class PropositionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
	model = Proposition

	def test_func(self):
		if self.request.user.is_captain:
			return True
		return False

'''
def DetailProposition(request, pk):
	proposition = Proposition.objects.get(id=pk)

	context = {'proposition' : proposition}

	return render(request, )
'''

class PropositionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Proposition
	fields = ['title', 'date_match', 'hour_beggin', 'lieu_match', 'name_stadium', ]


	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		if self.request.user.is_captain:
			return True
		return False

class PropositionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Proposition
	fields = ['title', 'date_match', 'hour_beggin', 'lieu_match', 'name_stadium', ]

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


class TrainingListView(LoginRequiredMixin, ListView):
	model = Training
	context_object_name = 'trainings'
	ordering = ['date_training']


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
#		form.instance.team_training = self.request.user.team
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

class TeamListView(ListView):
	model = Team
	context_object_name = 'teams'
	ordering = ['date_creation']


class TeamCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Team
	fields = ['libelle_team', 'nb_players_max']

	def form_valid(self, form):
		form.instance.creator =  self.request.user
		form.instance.nb_players = 0

		return super().form_valid(form)


	def test_func(self):
		if self.request.user.is_captain:
			return True
		return False

class TeamDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Team
	success_url = '/'

	def test_func(self):
		team = self.get_object()
		if (self.request.user.is_captain and team.creator == self.request.user):
			return True
		return False


# creer son match avant de le proposer 

'''
class MatchCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Match
	fields = ['real_date', 'hour_beggin', 'lieu_match']

	def form_valid(self, form):

		return super().form_valid(form)

	def test_func(self):
		if self.request.user.is_captain:
			return True
		return False
'''


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


# creer un entrainement avec seulement les équipes que j'ai creéé

@login_required
@user_passes_test(is_captain_check, login_url='home')
def SuggestTraining(request):
	if request.method=='POST':
		form = SuggestTrainingForm(request.user, request.POST)
		if form.is_valid():
			instance = form.save()
			messages.success(request, f'Your Training have been add !')
			return redirect('home')
	else : 
		form = SuggestTrainingForm(request.user)

	context = {'form' : form}

	return render(request, 'proposition/training_form.html', context)

'''
@login_required
def SeeMyTrainings(request):
	if request.user.is_captain:

		alltrainings=Training.objects.all()
		myteams = BelongToTeam.objects.filter(player=request.user)
		mytrainings=alltrainings.filter(team_training=request.)
'''


@login_required
@user_passes_test(is_captain_check, login_url='home')
def MyTeams(request):
	myteams=Team.objects.all()
	teams=myteams.filter(creator=request.user)

	context = {'teams':teams}

	return render(request, 'account/team_list.html', context)


'''
class ReserveCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Reserve

	def form_valid(self, form):
		form.instance.player = self.request.user
		form.instance.team = self.object
		return super().form_valid(form)

	def test_func(self):
		if self.request.user.is_captain:
			return True
		return False
'''



def Reservation(request, pk):
	proposition = Proposition.objects.get(id=pk)
	player = Account.objects.get(id=request.user.id)

	context={'proposition' : proposition, 'player' : player }

	if request.method=='POST':
		reserve = Reserve(team=team, player=player)
		reserve.save()
		messages.success(request, f'Proposition accepted !')

		return redirect('home')

	return render()

#	return HttpResponseRedirect(reverse('confirmation', kwargs={'pk': proposition.id}))

