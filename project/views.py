from django.shortcuts import render
from django.http import HttpResponse
from proposition.models import *
import datetime

def home(request):

	trainings=Training.objects.all()

	total_trainings=trainings.filter(team_training=request.user.team)
	total_trainings2=total_trainings.filter(date_training__gte=datetime.date.today())

	count_trainings=total_trainings2.count()

	context = {'count_trainings':count_trainings}

	return render(request, 'project/home.html', context)


def about(request):
	return render(request, 'project/about.html', {'title': 'About'})
