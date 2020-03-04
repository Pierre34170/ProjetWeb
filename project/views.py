from django.shortcuts import render
from django.http import HttpResponse
from proposition.models import *
from account.models import *
import datetime

def home(request):

	if request.user.is_authenticated:

		if request.user.is_captain:

			trainings=Training.objects.all()
			teams=Team.objects.filter(creator=request.user)

			total_trainings=trainings.filter(team_training__in=teams)
			total_trainings2=total_trainings.filter(date_training__gte=datetime.date.today())

			count_trainings=total_trainings2.count()

			context = {'count_trainings':count_trainings , 'total_trainings2' : total_trainings2}
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
			context = {'count_trainings':count_trainings , 'total_trainings' : total_trainings}
			return render(request, 'project/home.html', context)

	return render(request, 'project/home.html')