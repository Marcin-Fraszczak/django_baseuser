from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from .admin import CustomUserCreationForm

User = get_user_model()

class HomeView(View):
	def get(self, request):
		return render(request, "users/home.html")


class LogoutView(View):
	def get(self, request):
		logout(request)
		return redirect(reverse_lazy("users:home"))


class RegisterView(View):
	def get(self, request):
		form = CustomUserCreationForm()
		return render(request, "users/register.html", context={"form": form})

	def post(self, request):
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			try:
				user = form.save()
				login(request, user)
				return redirect(reverse_lazy("users:home"))
			except IntegrityError:
				form.add_error(None, "User with this email address already registered.")
		return render(request, "users/register.html", context={"form": form})
