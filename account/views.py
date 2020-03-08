from django.shortcuts import render, redirect
from django.contrib import messages
#from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, AccountUpdateForm
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from .models import Account
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

		context = {'a_form':a_form}

		if a_form.is_valid():
			a_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')

	else:
		a_form = AccountUpdateForm(instance=request.user)
	context = {
		'a_form': a_form
	}

	return render(request, 'account/profile.html', context)
	
