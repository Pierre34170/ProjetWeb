from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
from .models import Proposition, Reserve, Play
from account.models import Account
from team.models import Team, BelongToTeam
from .forms import ResearchMatchForm, ConfirmationMatchForm, PropositionModelForm
from django.contrib.auth.decorators import user_passes_test
import datetime


@login_required
def DetailProposition(request, pk):
	proposition = Proposition.objects.get(id=pk)

	context = {'proposition' : proposition}

	return render(request, 'proposition/proposition_detail.html', context )


class PropositionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

	template_name = 'proposition/proposition_form.html'
	form_class = PropositionModelForm


	def form_valid(self, form):

		form.instance.author = self.request.user

		return super().form_valid(form)

	def test_func(self):
		if self.request.user.is_captain:
			return True
		return False


class PropositionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Proposition
	fields = ['title', 'date_match', 'hour', 'address_match', 'name_stadium', ]

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
			allpropositions = Proposition.objects.filter(date_match= date)
			reservation = Reserve.objects.all()

			reservationtab=[]

			for i in reservation:
				reservationtab.append(i.proposition.id)

			propositions = allpropositions.exclude(id__in=reservationtab)

			context = {'form' : form, 'propositions' : propositions}
			return render(request, 'proposition/proposition_list.html', context)
	else:
		form = ResearchMatchForm()

	context = {'form' : form}

	return render(request, 'proposition/proposition_list.html', context)


@login_required
@user_passes_test(is_captain_check, login_url='home')
def Reservation(request, pk):
	proposition = Proposition.objects.get(id=pk)
	player = Account.objects.get(id=request.user.id)

	context={'proposition' : proposition, 'player' : player }

	if request.method=='POST':
		form = ConfirmationMatchForm(request.user, request.POST)
		if form.is_valid():
			instance = form.save()
			instance.game = proposition
			instance.save()
			reserve = Reserve(proposition=proposition, player=player)
			reserve.save()
			messages.success(request, f'Proposition accepted !')
			return redirect('home')
	else :
		form = ConfirmationMatchForm(request.user)

	context = {'proposition' : proposition, 'player' : player, 'form' : form}

	return render(request, 'proposition/reserve_confirm.html', context)


@login_required
@user_passes_test(is_captain_check, login_url='home')
def MyResponse(request):
	propositions = Proposition.objects.filter(author=request.user)
	propositionfutur = propositions.filter(date_match__gte=datetime.date.today())
	myresponse = Reserve.objects.filter(proposition__in=propositionfutur)
	myteams = Team.objects.filter(creator=request.user)
	prop = Play.objects.filter(team__in=myteams)

	proptab = []

	for i in prop:
		proptab.append(i.game)

	response = myresponse.exclude(proposition__in=proptab)


	context = {'response' : response}

	return render(request, 'proposition/proposition_response.html', context)


@login_required
def DetailMatch(request, pk):
	proposition = Proposition.objects.get(id=pk)
	if request.method=='POST':
		form = ConfirmationMatchForm(request.user, request.POST)
		if form.is_valid():
			instance = form.save()
			instance.game = proposition
			instance.save()
			messages.success(request, f'Now, you can play !')
			return redirect('proposition_response')
	else:
		form = ConfirmationMatchForm(request.user)

	context = {'proposition' : proposition, 'form' : form}

	return render(request, 'proposition/matchs_detail.html', context )


@login_required
def MyMatchs(request):
	if request.user.is_captain:
		propositions = Proposition.objects.filter(author=request.user)
		propositionfutur = propositions.filter(date_match__gte=datetime.date.today())
		response = Reserve.objects.filter(proposition__in=propositionfutur)
		responses = Reserve.objects.filter(player=request.user)

		myresponses = response.union(responses)

		myresponsestab = []

		for i in myresponses:
			myresponsestab.append(i.proposition)

		context = {'myresponsestab' : myresponsestab}

		return render(request, 'proposition/matchs.html', context)

	else:
		teams = BelongToTeam.objects.filter(player=request.user)

		myteamtab = []
		for i in teams:
			myteamtab.append(i.team)

		mymatchs = Play.objects.filter(team__in=myteamtab)

		myresponsestab = []

		for i in mymatchs:
			myresponsestab.append(i.game)

		context = {'myresponsestab' : myresponsestab}

		return render(request, 'proposition/matchs.html', context)








