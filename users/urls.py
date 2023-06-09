from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
	path('', views.HomeView.as_view(), name='home'),
	path('users/register/', views.RegisterView.as_view(), name='register'),
	path('users/logout/', views.LogoutView.as_view(), name='logout'),
]
