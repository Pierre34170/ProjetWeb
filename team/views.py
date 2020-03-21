from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.generic import CreateView
from .filters import TeamFilter
from .models import *
from django.contrib.auth.decorators import user_passes_test




def is_captain_check(user):
	return user.is_captain


class TeamCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Team
	fields = ['name_team', 'number_players_max']

	def form_valid(self, form):
		form.instance.creator =  self.request.user
		form.instance.number_players = 0

		return super().form_valid(form)


	def test_func(self):
		if self.request.user.is_captain:
			return True
		return False



@login_required
@user_passes_test(is_captain_check, login_url='home')
def MyTeams(request):
	myteams=Team.objects.all()
	teams=myteams.filter(creator=request.user)

	context = {'teams':teams}

	return render(request, 'team/team_list.html', context)


@login_required
@user_passes_test(is_captain_check, login_url='home')

def MyTeamDetail(request, pk):
	team = Team.objects.get(id=pk)
	myplayers = BelongToTeam.objects.filter(team=team)

	myplayerstab=[]

	for i in myplayers:
		myplayerstab.append(i)

	playerbelongtoteam = myplayerstab

	context={'playerbelongtoteam':playerbelongtoteam}

	return render(request, 'team/see_my_team.html', context)


@login_required
@user_passes_test(is_captain_check, login_url='home')
def DeleteMyPlayers(request, pk):


	player = BelongToTeam.objects.get(id=pk)
	myteam = player.team

	if request.method=="POST":
		myteam.nb_players = myteam.nb_players-1
		myteam.save() 
		player.delete()
		messages.success(request, f'Player deleted !')
		return redirect('home')

	context = {'player':player}


	context = {}
	return render(request, 'team/delete_player.html',context)


@login_required
@user_passes_test(is_captain_check, login_url='home')
def DeleteMyTeam(request, pk):


	team = Team.objects.get(id=pk)

	if request.method=="POST":
		team.delete()
		messages.success(request, f'Team deleted !')
		return redirect('home')

	context = {'team':team}

	return render(request, 'team/delete_team.html',context)


@login_required
def ResearchTeam(request):

	myteams = BelongToTeam.objects.filter(player=request.user)
	myteamstab=[]
	for i in myteams:
		myteamstab.append(i.team.name_team)

	teams = Team.objects.exclude(name_team__in=myteamstab)


	myFilter = TeamFilter(request.GET, queryset=teams)
	teams  = myFilter.qs

	context = {'teams' : teams, 'myFilter' : myFilter }

	return render(request, 'team/find_team.html', context)



@login_required
def JoinTeam(request, pk):
	team = Team.objects.get(id=pk)
	player = Account.objects.get(id= request.user.id)

	context={'team' : team, 'player' : player }


	if request.method=='POST':
		if (team.number_players < (team.number_players_max)):
			team.number_players = team.number_players +1
			team.save()
			belongto = BelongToTeam(team=team, player=player)
			belongto.save()
			messages.success(request, f'Team joined !')

			return redirect('home')
		messages.success(request, f'Sorry this team is already complete')
		return render(request,'account/join_team.html', context)

	return render(request, 'team/join_team.html', context)









