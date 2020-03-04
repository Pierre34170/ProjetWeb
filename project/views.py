from django.shortcuts import render
from django.http import HttpResponse
from proposition.models import *
import datetime

def home(request):

	if request.user.is_authenticated:
		trainings=Training.objects.all()
		teams=Team.objects.filter(creator=request.user)

		total_trainings=trainings.filter(team_training__in=teams)
		total_trainings2=total_trainings.filter(date_training__gte=datetime.date.today())

		count_trainings=total_trainings2.count()

		context = {'count_trainings':count_trainings}
		return render(request, 'project/home.html', context)

	return render(request, 'project/home.html')