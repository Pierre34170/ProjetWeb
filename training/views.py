from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.generic import (
	ListView, 
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
	)
from .views import *
from team.models import * 
from .models import *
from django.contrib.auth.decorators import user_passes_test
from .forms import SuggestTrainingForm
import datetime

def is_captain_check(user):
	return user.is_captain




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


class TrainingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Training
	fields = ['date_training', 'hour_training', 'type_training', 'team_training']

	def form_valid(self, form):
		return super().form_valid(form)

	def test_func(self):
		training = self.get_object()
		if (self.request.user.is_captain):
			return True
		return False


class TrainingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Training
	success_url = '/'

	def test_func(self):
		training = self.get_object()
		if (self.request.user.is_captain):
			return True
		return False



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

	return render(request, 'training/training_form.html', context)


@login_required
def MyTrainings(request):

	if request.user.is_captain:

		trainings=Training.objects.all()
		teams=Team.objects.filter(creator=request.user)
		total_trainings1=trainings.filter(team_training__in=teams)
		total_trainings2=total_trainings1.filter(date_training__gte=datetime.date.today())
		total_trainings=total_trainings2.order_by('-date_training')

		context = { 'total_trainings' : total_trainings }
		return render(request, 'training/training_list.html', context)

	else :
		trainings=Training.objects.all()
		teams = BelongToTeam.objects.filter(player=request.user)

		mytrainingtab=[]

		for i in teams:
			mytrainingtab.append(i.team)

		mytrainings=trainings.filter(team_training__in=mytrainingtab)

		total_trainings1=mytrainings.filter(date_training__gte=datetime.date.today())
		total_trainings=total_trainings1.order_by('date_training')

		context = {'total_trainings' : total_trainings}
		return render(request, 'training/training_list.html', context)

