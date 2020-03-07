from django import forms
from .models import Training
from team.models import Team
import datetime
import re



class SuggestTrainingForm(forms.ModelForm):
#	teams=Team.objects.filter(Team.creator=='pierre34')
#	team_training = forms.ModelChoiceField(queryset=teams)

	class Meta:
		model = Training
		fields = ['date_training', 'hour_training', 'type_training', 'team_training']

	def clean(self):
		cleaned_data = super().clean()
		print(cleaned_data)
		date_training = cleaned_data.get("date_training")

		pattern = '^[0-9]{2,4}-[0-9]{1,2}-[0-9]{1,2}$'
		resultdate = re.match(pattern, str(date_training))

		if resultdate:
			if date_training < datetime.date.today():
				raise forms.ValidationError('This date is already passed !')

		return cleaned_data

	def __init__(self, user,*args, **kwargs):
		super(SuggestTrainingForm, self).__init__(*args, **kwargs)
		self.fields['team_training'].queryset = Team.objects.filter(creator=user)



