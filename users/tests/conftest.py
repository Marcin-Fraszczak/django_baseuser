import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import Client
from django.urls import reverse

from bs4 import BeautifulSoup as Bs
from datetime import datetime

from users.models import Idea


def pytest_html_report_title(report):
	report.title = "Test report task_1 and task_2 of BitByBit recruitment process."


@pytest.fixture
def client():
	client = Client()
	return client


@pytest.fixture
def user():
	user = get_user_model().objects.create(username="test_user@domain.com")
	return user


@pytest.fixture
def home_url():
	return "users:home"


@pytest.fixture
def ideas_url():
	return "users:ideas"


@pytest.fixture
def profile_url():
	return "users:ideas"


@pytest.fixture
def register_url():
	return "users:register"


@pytest.fixture
def register_form(client, register_url):
	form_id = "registration_form"
	response = client.get(reverse(register_url))
	soup = Bs(response.content, 'html.parser')
	return soup.find(id=form_id)


@pytest.fixture
def form_id():
	return "numbers_sorting_form"


@pytest.fixture
def input_id():
	return "numbers_sorting_input"


@pytest.fixture
def no_input():
	return "This field is required."


@pytest.fixture
def idea(user):
	idea = Idea(
		title="Idea title",
		content="Idea content",
		created=datetime.now(),
		owner=user,
	)
	return idea


@pytest.fixture
def email_backend_setup(settings):
	settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'


@pytest.fixture
def prepare_grouped_users():
	emails = ['1@1.com', '2@2.com', '3@3.com', '4@4.com']
	group_names = ['H/Div', 'H/Sec', 'H/Ple', "No group"]
	users = []
	for data in zip(emails, group_names):
		user = get_user_model().objects.create(username=data[0])
		group = Group.objects.create(name=data[1])
		user.groups.add(group)
		user.save()
		group.save()
		users.append(user)
	return users