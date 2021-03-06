from django.db import models
from team.models import Team
from django.urls import reverse

class Training(models.Model):
	date_training = models.DateField(verbose_name="Date")
	hour_training = models.TimeField(verbose_name="Hour")
	type_training = models.CharField(verbose_name="Type", max_length=300)
	team_training = models.ForeignKey(Team, verbose_name="Team", on_delete=models.CASCADE)

	def __str__(self):
		return self.type_training

	def get_absolute_url(self):
		return reverse('training_detail', kwargs={'pk': self.pk})
