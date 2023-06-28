from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect

from .email import send_message
from .forms import RegisterForm, NumberForm, IdeaForm
from .models import Idea
from .validators import normalize_email

User = get_user_model()


class HomeView(View):
	def get(self, request):
		form = NumberForm()
		return render(request, "home.html", context={"form": form})

	def post(self, request):
		form = NumberForm(request.POST)
		if form.is_valid():
			try:
				to_sort = form.cleaned_data.get("in_data").split(",")
				to_sort_cleaned = map(float, to_sort)
				result = sorted(to_sort_cleaned)
				result = [int(item) if int(item) == item else item for item in result]
				return render(request, "home.html", context={"form": form, "result": result})
			except ValueError as e:
				form.add_error(None, "Invalid input!")

		else:
			form.add_error(None, "No input!")
		return render(request, "home.html", context={"form": form})


class LogoutView(View):
	def get(self, request):
		logout(request)
		return redirect(reverse_lazy("users:home"))


class RegisterView(View):
	def get(self, request):
		form = RegisterForm()
		return render(request, "users/register.html", context={"form": form})

	def post(self, request):
		form = RegisterForm({
			"username": normalize_email(request.POST.get('username')),
			"group": request.POST.get('group'),
			"password": request.POST.get('password')
		})

		if form.is_valid():
			logout(request)
			try:
				group = form.cleaned_data.get('group')
				existing_group = Group.objects.get(name=group)
				if not existing_group:
					form.add_error("group", "No such group!")
					return render(request, "users/register.html", context={"form": form})
				user = form.save()
				existing_group.user_set.add(user)
				user.save()
				login(request, user)
				messages.success(request, "Successfully registered user.")
				return redirect(reverse_lazy("users:profile"))
			except IntegrityError:
				form.add_error("email", "User with this email address already registered.")
			except Group.DoesNotExist:
				form.add_error("group", "No such group!")
		return render(request, "users/register.html", context={"form": form})


class LoginView(View):
	def get(self, request):
		form = AuthenticationForm()
		return render(request, "users/login.html", context={"form": form})

	def post(self, request):
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			logout(request)
			user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
			if user:
				login(request, user)
				return redirect(reverse_lazy("users:profile"))
		form.add_error(None, "Invalid credentials")
		return render(request, "users/login.html", context={"form": form})


class IdeasView(LoginRequiredMixin, View):
	def get(self, request):
		form = IdeaForm()
		ideas = Idea.objects.all().order_by('-created')[:5]
		return render(request, "users/ideas.html", context={"form": form, "ideas": ideas})

	def post(self, request):
		user = request.user
		if "delete_idea" in request.POST:
			idea_pk = request.POST.get('delete_idea')
			Idea.objects.filter(pk=idea_pk).delete()
		elif "subscribe" in request.POST:
			user.subscribed = True
			user.save()
		elif "unsubscribe" in request.POST:
			user.subscribed = False
			user.save()
		else:
			form = IdeaForm(request.POST)
			if form.is_valid():
				idea = form.save(commit=False)
				idea.owner = user
				idea.save()

				recipients = [user.username for user in User.objects.filter(
					Q(subscribed=True) | Q(groups__name="H/Div") | Q(groups__name="H/Sec")
				)]
				send_message(recipients, idea)

			else:
				form.add_error(None, "Invalid input")
				return render(request, "users/ideas.html", context={"form": form})
		return redirect("users:ideas")


class ProfileView(LoginRequiredMixin, View):
	def get(self, request):
		return render(request, "users/profile.html")

	def post(self, request):
		user = request.user
		if "subscribe" in request.POST:
			user.subscribed = True
			user.save()
		elif "unsubscribe" in request.POST:
			user.subscribed = False
			user.save()

		return redirect("users:profile")
