from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from re import sub as re_sub


class CustomUserManager(BaseUserManager):
	def _create_user(self, username, password, is_staff, is_superuser, **extra_fields):
		if not username:
			raise ValueError('Users must have an email address')
		now = timezone.now()
		username = self.normalize_email(username)
		user = self.model(
			username=username,
			is_staff=is_staff,
			is_active=True,
			is_superuser=is_superuser,
			last_login=now,
			date_joined=now,
			**extra_fields
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, username, password, **extra_fields):
		return self._create_user(username, password, False, False, **extra_fields)

	def create_superuser(self, username, password, **extra_fields):
		user = self._create_user(username, password, True, True, **extra_fields)
		return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
	username = models.EmailField(max_length=254, unique=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	last_login = models.DateTimeField(null=True, blank=True)
	date_joined = models.DateTimeField(auto_now_add=True)
	subscribed = models.BooleanField(default=False)

	USERNAME_FIELD = 'username'
	EMAIL_FIELD = 'username'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()

	def __str__(self):
		return self.username


class Idea(models.Model):
	title = models.CharField(max_length=128)
	content = models.CharField(max_length=500)
	created = models.DateTimeField(auto_now=True)
	owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.title}"
