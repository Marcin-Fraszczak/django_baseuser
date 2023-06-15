from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import validate_password

from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required fields."""
	password = forms.CharField(
		label="Password",
		widget=forms.PasswordInput,
	)

	class Meta:
		model = CustomUser
		fields = ["email", ]

	def save(self, commit=True):
		# Save the provided password in hashed format
		print("saving")
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user

	def clean_password(self):
		pass
		# checks provided password against both build-in and custom password validators
		# password = self.cleaned_data['password']
		# validate_password(password)


class CustomUserChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	disabled password hash display field.
	"""

	password = ReadOnlyPasswordHashField()

	class Meta:
		model = CustomUser
		fields = ["email", "password", "is_active", "is_admin"]
