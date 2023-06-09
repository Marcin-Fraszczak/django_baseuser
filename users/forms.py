from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomUser
from .validators import custom_password_validator


class CustomUserCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required fields."""
	password = forms.CharField(
		label="Password",
		widget=forms.PasswordInput,
		validators=[custom_password_validator]
	)

	class Meta:
		model = CustomUser
		fields = ["email", ]

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user

	# def clean(self):
	# 	cleaned_data = super().clean()
	# 	email = cleaned_data.get("email")
	# 	password = cleaned_data.get("password")
	# 	if password and email:
	# 		similarity_password_validator(password, email)


class CustomUserChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	disabled password hash display field.
	"""

	password = ReadOnlyPasswordHashField()

	class Meta:
		model = CustomUser
		fields = ["email", "password", "is_active", "is_admin"]
