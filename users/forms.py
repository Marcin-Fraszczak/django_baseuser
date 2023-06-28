from django.contrib.auth.password_validation import validate_password
from django import forms
from .models import CustomUser, Idea

GROUPS_CHOICES = [
	("No group", "No group"),
	("H/Div", "H/Div"),
	("H/Sec", "H/Sec"),
	("H/Ple", "H/Ple"),
]


class RegisterForm(forms.ModelForm):
	password = forms.CharField(
		label="Password",
		widget=forms.PasswordInput,
	)
	group = forms.ChoiceField(
		label="Group",
		choices=GROUPS_CHOICES,
	)

	class Meta:
		model = CustomUser
		fields = ('username',)

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user

	def clean_password(self):
		password = self.cleaned_data['password']
		validate_password(password)
		return password



class NumberForm(forms.Form):
	in_data = forms.CharField(
		label="Specify numbers to sort separated by coma.",
		widget=forms.TextInput(
			attrs={
				"placeholder": "Example: 12, 2, 101, -4 ...",
				"class": "my-3",
			})
	)


class IdeaForm(forms.ModelForm):
	class Meta:
		model = Idea
		fields = ("title", "content")