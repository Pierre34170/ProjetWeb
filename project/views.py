from django.shortcuts import render
from django.http import HttpResponse
from proposition.models import *
from account.models import *
from training.models import *
from team.models import *
import datetime

def home(request):

	if request.user.is_authenticated:

		if request.user.is_captain:

			trainings=Training.objects.all()
			teams=Team.objects.filter(creator=request.user)
			total_trainings1=trainings.filter(team_training__in=teams)
			total_trainings=total_trainings1.filter(date_training__gte=datetime.date.today())
			count_trainings=total_trainings.count()

			propositions = Proposition.objects.filter(author=request.user)
			propositionfutur = propositions.filter(date_match__gte=datetime.date.today())
			response = Reserve.objects.filter(proposition__in=propositionfutur)
			responses = Reserve.objects.filter(player=request.user)
			myresponses = response.union(responses)
			count_matchs = myresponses.count()

			context = {'count_trainings':count_trainings, 'count_matchs' : count_matchs}
			return render(request, 'project/home.html', context)

		else :
			trainings=Training.objects.all()
			teams = BelongToTeam.objects.filter(player=request.user)

			mytrainingtab=[]

			for i in teams:
				mytrainingtab.append(i.team)

			mytrainings=trainings.filter(team_training__in=mytrainingtab)

			total_trainings=mytrainings.filter(date_training__gte=datetime.date.today())
			count_trainings=total_trainings.count()

			myteamtab = []
			for i in teams:
				myteamtab.append(i.team)

			mymatchs = Play.objects.filter(team__in=myteamtab)

			count_matchs = mymatchs.count()
			
			context = {'count_trainings':count_trainings , 'count_matchs' : count_matchs }
			return render(request, 'project/home.html', context)

	return render(request, 'project/home.html')





	