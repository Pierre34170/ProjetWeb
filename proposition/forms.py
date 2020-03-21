from django import forms
from .models import Proposition, Play
from team.models import Team
import datetime
import re


class PropositionModelForm(forms.ModelForm):
	date_match = forms.DateField(widget=forms.TextInput({'placeholder': 'YYYY-MM-DD'}))
	hour = forms.TimeField(widget=forms.TextInput({'placeholder': 'HH:MM:SS'}))
	
	class Meta:
		model = Proposition
		fields = ['title', 'date_match', 'hour', 'address_match', 'name_stadium', ]


	def clean(self):
		cleaned_data = super().clean()
		print(cleaned_data)
		date_match = cleaned_data.get("date_match")

		pattern = '^[0-9]{2,4}-[0-9]{1,2}-[0-9]{1,2}$'
		resultdate = re.match(pattern, str(date_match))

		if resultdate:
			if date_match < datetime.date.today():
				raise forms.ValidationError('This date is already passed !')

		return cleaned_data


class ResearchMatchForm(forms.ModelForm):
	date_match = forms.DateField(widget=forms.TextInput({'placeholder': 'YYYY-MM-DD'}))

	class Meta:
		model = Proposition
		fields =['date_match']

	def clean(self):
		cleaned_data = super().clean()
		print(cleaned_data)
		date_match = cleaned_data.get("date_match")

		pattern = '^[0-9]{2,4}-[0-9]{1,2}-[0-9]{1,2}$'
		resultdate = re.match(pattern, str(date_match))

		if resultdate:
			if date_match < datetime.date.today():
				raise forms.ValidationError('This date is already passed !')

		return cleaned_data


class ConfirmationMatchForm(forms.ModelForm):
	class Meta:
		model = Play
		fields = ['team']

	def __init__(self, user,*args, **kwargs):
		super(ConfirmationMatchForm, self).__init__(*args, **kwargs)
		self.fields['team'].queryset = Team.objects.filter(creator=user)




