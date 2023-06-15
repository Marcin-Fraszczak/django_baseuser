from re import sub as re_sub

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class CustomUserManager(BaseUserManager):

	# from https://dev.maxmind.com/minfraud/normalizing-email-addresses-for-minfraud
	@classmethod
	def normalize_email(cls, email):
		print("normalizing...")
		print(email)
		try:
			# 1.  Trim whitespace from both ends of the address.
			# 2.  Lowercase the address.
			# 3.  Find the local part of the email and the domain.
			email_name, domain_part = email.strip().lower().rsplit("@", 1)
			# 4.  Trim the whitespace from the domain.
			# 5.  Trim any number of periods from the end of the domain.
			domain_part = domain_part.lstrip().rstrip('.')
			# 6.  Convert international domain names to ASCII.
			domain_part = domain_part.encode("idna")
			# 7.  Check for common typos.
			"""not implemented"""
			# 8.  Remove repetitions of '.com'.
			# 9.  Remove any characters after '.com'.
			re_sub('\.com[a-z0-9]+', '.com', domain_part)
			# 10. Remove leading digits in 'gmail.com'.
			re_sub('[0-9]+gmail.com', 'gmail.com', domain_part)
			# 11. For fastmail.com replace the email local part with the subdomain.
			"""not implemented"""
			# 12. Remove alias parts from the local part.
			"""not implemented"""
			# 13. Put the local part and the domain part back together.
			email = f"{email_name}@{domain_part}"
			# 14. Calculate the MD5 hash.
			"""not implemented"""
			print(email)
			return email
		except ValueError:
			return ""


	def create_user(self, email, password=None):
		"""Creates and saves a User with the given email and password."""
		if not email:
			raise ValueError("Users must have an email address")

		user = self.model(
			email=self.normalize_email(email),
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password=None):
		"""Creates and saves a superuser with the given email and password."""
		user = self.create_user(
			email,
			password=password,
		)
		user.is_admin = True
		user.save(using=self._db)
		return user


class CustomUser(AbstractBaseUser):
	email = models.EmailField(
		verbose_name="email address",
		max_length=255,
		unique=True,
	)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = CustomUserManager()

	USERNAME_FIELD = "email"

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		"""Does the user have a specific permission?"""
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"""Does the user have permissions to view the app `app_label`?"""
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"""Is the user a member of staff?"""
		# Simplest possible answer: All admins are staff
		return self.is_admin
