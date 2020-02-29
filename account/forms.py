from django import forms
from django.contrib.auth.forms import UserCreationForm

from account.models import Account



class RegistrationForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = Account
		fields = ('username', 'is_captain', 'first_name', 'last_name', 'email','numTel', 'password1', 'password2')




class AccountUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	numTel = forms.CharField(required=True)

	class Meta:
		model = Account
		fields = ('email', 'username', 'first_name', 'last_name', 'numTel', 'team')


'''	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except Account.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' %account.email)

	def clean_username(self):
		if self.is_valid():
			username = self.cleaned_data['username']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
		except Account.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' %account.username)

	def clean_first_name(self):
		if self.is_valid():
			first_name = self.cleaned_data['first_name']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(first_name=first_name)
		except Account.DoesNotExist:
			return first_name
		raise forms.ValidationError('first name "%s" is already in use.' %account.first_name)

	def clean_last_name(self):
		if self.is_valid():
			last_name = self.cleaned_data['last_name']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(last_name=last_name)
		except Account.DoesNotExist:
			return last_name
		raise forms.ValidationError('last name "%s" is already in use.' %account.last_name)


	def clean_numTel(self):
		if self.is_valid():
			numTel = self.cleaned_data['numTel']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(numTel=numTel)
		except Account.DoesNotExist:
			return numTel
		raise forms.ValidationError('this num "%s" is already in use.' %account.numTel)
'''



