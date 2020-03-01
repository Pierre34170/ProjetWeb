from django.db import models
from account.models import Account, Team
from django.utils import timezone
from django.urls import reverse


class Match(models.Model):
	real_date = models.DateField()
	hour_beggin = models.TimeField()
	lieu_match = models.CharField(max_length=300)

	def __str__(self):
		return (self.lieu_match)

	def get_absolute_url(self):
		return reverse('home')
		

class Training(models.Model):
	date_training = models.DateField()
	hour_training = models.TimeField()
	type_training = models.CharField(max_length=300)
	team_training = models.ForeignKey(Team, on_delete=models.CASCADE)

	def __str__(self):
		return self.type_training

	def get_absolute_url(self):
		return reverse('training_detail', kwargs={'pk': self.pk})

		

class Stadium(models.Model):
	libelle_stadium = models.CharField(max_length=300)
	lieu_stadium = models.CharField(max_length=300)

	def __str__(self):
		return (self.libelle_stadium)


class Proposition(models.Model):
	title = models.CharField(max_length=300)
	date_posted = models.DateTimeField(default=timezone.now)
	date_match = models.DateField()
	match = models.ForeignKey(Match, null = True, on_delete=models.CASCADE)
	author = models.ForeignKey(Account, null = True, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('proposition_detail', kwargs={'pk': self.pk})


class Play(models.Model):
	game = models.ForeignKey(Match, on_delete=models.CASCADE)
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	score = models.CharField(max_length=10)

'''
class Response(models.Model):
	demandeur = models.ForeignKey(Account, on_delete=models.CASCADE)
	accepteur = models.ForeignKey(Account, on_delete=models.CASCADE)
	date_response = models.DateTimeField(default=timezone.now)

'''