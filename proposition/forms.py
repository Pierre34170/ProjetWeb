from django import forms
from .models import Proposition
import datetime
import re




class OrganizeForm(forms.ModelForm):
	class Meta:
		model = Proposition
		fields = ('title', 'date_posted', 'date_match')



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