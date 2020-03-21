from django import forms
from django.contrib.auth.forms import UserCreationForm

from account.models import Account
#from .models import Profile


class RegistrationForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = Account
		fields = ('username', 'is_captain', 'first_name', 'last_name', 'city', 'email','numTel', 'password1', 'password2')




class AccountUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	numTel = forms.CharField(required=True)

	class Meta:
		model = Account
		fields = ('email', 'username', 'first_name', 'last_name', 'city', 'numTel', 'image')



