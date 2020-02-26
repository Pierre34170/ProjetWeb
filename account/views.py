from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, AccountUpdateForm
from django.contrib.auth.decorators import login_required


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
			login(request, account)
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

		if a_form.is_valid():
			a_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')

	else:
		a_form = AccountUpdateForm(instance=request.user)

	context = {
		'a_form': a_form,
	}

	return render(request, 'account/profile.html', context)
	



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