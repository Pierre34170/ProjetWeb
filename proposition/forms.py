from django import forms
from .models import Proposition





class OrganizeForm(forms.ModelForm):
	class Meta:
		model = Proposition
		fields = ('title', 'date_posted', 'date_match')

