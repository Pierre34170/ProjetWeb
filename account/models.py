from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.urls import reverse


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, first_name, last_name, is_captain, city, numTel, password=None):
#			raise ValueError("Users must have an email address")
#		if not username:
#			raise ValueError("Users must have an username")
#		if not first_name:
#			raise ValueError("Users must have an first_name")
#		if not last_name:
#			raise ValueError("Users must have an last_name")
#		if not is_captain:
#			raise ValueError("Users must fill the field")
#		if not numTel:
#			raise ValueError("Users must fill the field")

		user = self.model(
			email=self.normalize_email(email),
			username=username,
			first_name=first_name,
			last_name=last_name,
			is_captain=is_captain,
			city=city,
			numTel=numTel,
			)

		user.set_password(password)
		user.save(using=self._db)
		return user 

	def create_superuser(self, email, username, first_name, last_name, is_captain, city, numTel, password):
		user = self.create_user(
			email=self.normalize_email(email),
			username=username,
			first_name=first_name,
			last_name=last_name,
			is_captain=is_captain,
			city=city,
			numTel=numTel,
			password=password
			)

		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

'''
class Team (models.Model):
	libelle_team = models.CharField(max_length=30)
	date_creation = models.DateTimeField(default=timezone.now)
#	plays = models.ManyToManyField(Match, through='Play' )

	def __str__(self):
		return self.libelle_team
'''

class Team (models.Model):
	libelle_team = models.CharField(max_length=30, unique=True)
#	nb_players = models.PositiveIntegerField()
	date_creation = models.DateTimeField(verbose_name='date creation', auto_now=True)

	def __str__(self):
		return self.libelle_team

	def get_absolute_url(self):
		return reverse('home')
'''
class BelongTo(models.Model):

'''


class Account(AbstractBaseUser):
	username = models.CharField(max_length=30, unique=True)
	first_name = models.CharField(max_length=30, unique=False)
	last_name = models.CharField(max_length=30, unique=False)
	email = models.EmailField(verbose_name="email", max_length=60, unique=True)
	is_captain = models.BooleanField(default=False)
	city = models.CharField(max_length=30)
	team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
	numTel = models.CharField(max_length=10, unique=True)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username','first_name','last_name','is_captain', 'city', 'numTel']

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_Label):
		return True



