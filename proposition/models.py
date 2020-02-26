from django.db import models
from account.models import Account
from django.utils import timezone



class Match(models.Model):
	real_date = models.DateTimeField()
	lieu_match = models.CharField(max_length=300)

	def __str__(self):
		return self.lieu_match
		

class Stadium(models.Model):
	libelle_stadium = models.CharField(max_length=300)
	lieu_stadium = models.CharField(max_length=300)

	def __str__(self):
		return self.libelle_stadium


class Proposition(models.Model):
	title = models.CharField(max_length=300)
	date_posted = models.DateTimeField(default=timezone.now)
	date_match = models.DateTimeField()
	match = models.ForeignKey(Match, on_delete=models.CASCADE)
	author = models.ForeignKey(Account, on_delete=models.CASCADE)

	def __str__(self):
		return self.title


class Play(models.Model):
	game = models.ForeignKey(Match, on_delete=models.CASCADE)
	team = models.ForeignKey(Account, on_delete=models.CASCADE)
	score = models.CharField(max_length=10)


