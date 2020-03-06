from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, AccountUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from .filters import TeamFilter
from .models import Team, Account, BelongToTeam
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test


def is_captain_check(user):
	return user.is_captain


@unauthenticated_user
def registration_view(request):
	context={}
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			messages.success(request, f'Account created ! Now you can log in')
			return redirect('login')
		else:
			context['registration_form']=form
	else:
		form = RegistrationForm()
		context['registration_form']=form
	return render(request, 'account/register.html', {'form': form})



@login_required
def profile_view(request):
	if request.method == 'POST':
		a_form = AccountUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm( request.POST, request.FILES, instance=request.user.profile)

		context = {'a_form':a_form, 'p_form':p_form}

		if a_form.is_valid() and p_form.is_valid():
			a_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')

	else:
		a_form = AccountUpdateForm(instance=request.user)
		p_form= ProfileUpdateForm(instance=request.user.profile)
	context = {
		'a_form': a_form,
		'p_form': p_form
	}

	return render(request, 'account/profile.html', context)
	


@login_required
def ResearchTeam(request):

	myteams = BelongToTeam.objects.filter(player=request.user)
	myteamstab=[]
	for i in myteams:
		myteamstab.append(i.team.libelle_team)

	teams = Team.objects.exclude(libelle_team__in=myteamstab)

#	team = teams.filter(libelle_team__ne=libelle_team)

	myFilter = TeamFilter(request.GET, queryset=teams)
	teams  = myFilter.qs

	context = {'teams' : teams, 'myFilter' : myFilter }

	return render(request, 'account/find_team.html', context)



@login_required
def JoinTeam(request, pk):
	team = Team.objects.get(id=pk)
	player = Account.objects.get(id= request.user.id)

	context={'team' : team, 'player' : player }


	if request.method=='POST':
		if (team.nb_players < (team.nb_players_max)):
			team.nb_players = team.nb_players +1
			team.save()
			belongto = BelongToTeam(team=team, player=player)
			belongto.save()
			messages.success(request, f'Team joined !')

			return redirect('home')
		messages.success(request, f'Sorry this team is already complete')
		return render(request,'account/join_team.html', context)

	return render(request, 'account/join_team.html', context)


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

	return render(request, 'account/see_my_team.html', context)


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
	return render(request, 'account/delete_player.html',context)


@login_required
@user_passes_test(is_captain_check, login_url='home')
def DeleteMyTeam(request, pk):


	team = Team.objects.get(id=pk)

	if request.method=="POST":
		team.delete()
		messages.success(request, f'Team deleted !')
		return redirect('home')

	context = {'team':team}

	return render(request, 'account/delete_team.html',context)



#def profile_view(request):
#
#	if not request.user.is_authenticated:
#		return redirect("login")
#
#	context = {}
#
#	if request.POST:
#		form = AccountUpdateForm(request.POST, instance=request.user)
#		if form.is_valid():
#			form.save()
#	else:
#		form = AccountUpdateForm(
#				initial = {
#				"email": request.user.email,
#				"username": request.user.username,
#				"first_name": request.user.first_name,
#				"last_name": request.user.last_name,
#				"numTel": request.user.numTel,
#				}
#			)
#
#	context['account_form'] = form 
#	return render(request, 'account/profile.html', context)



#def logout_view(request):
#	logout(request)
#	return redirect('home')