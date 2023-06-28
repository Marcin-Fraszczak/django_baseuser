from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
	path('', views.HomeView.as_view(), name='home'),
	path('users/register/', views.RegisterView.as_view(), name='register'),
	path('users/login/', views.LoginView.as_view(), name='login'),
	path('users/logout/', views.LogoutView.as_view(), name='logout'),
	path('users/profile/', views.ProfileView.as_view(), name='profile'),
	path('users/ideas/', views.IdeasView.as_view(), name='ideas'),
]
