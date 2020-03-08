from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.urls import reverse
from PIL import Image



class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, first_name, last_name, is_captain, city, numTel, password=None):

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
			password=password,
			)

		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	username = models.CharField(max_length=30, unique=True)
	first_name = models.CharField(max_length=30, unique=False)
	last_name = models.CharField(max_length=30, unique=False)
	email = models.EmailField(verbose_name="email", max_length=60, unique=True)
	is_captain = models.BooleanField(default=False)
	city = models.CharField(max_length=30)
	numTel = models.CharField(max_length=10, unique=True)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')
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


	def save(self, *args, **kwargs):
		super().save()

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)

