"""
Unit tests for part 2 of the recruitment task (email functionalities).

Run command with report creation:
pytest --html=templates/tests/report.html --self-contained-html

"""
import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from bs4 import BeautifulSoup as Bs


@pytest.mark.django_db
def test_email_is_sent_when_submitting_new_idea(
		client, ideas_url, user, idea, prepare_grouped_users, email_backend_setup):
	help_text = f"""
		Tests if email is sent after posting correct form data at: '{ideas_url}'
	"""
	print(help_text)

	client.force_login(user)
	response = client.post(
		reverse(ideas_url),
		{
			"title": idea.title,
			"content": idea.content
		}
	)

	assert response.status_code == 302
	assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_email_has_correct_recipients(client, ideas_url, user, idea, prepare_grouped_users, email_backend_setup):
	user.subscribed = True
	user.save()
	correct_recipients = [
		prepare_grouped_users[0].username,
		prepare_grouped_users[1].username,
		user.username
	]
	help_text = f"""
		Tests if email is sent to correct recipients at: '{ideas_url}'
		Correct recipients belong to 'H/Div' or 'H/Sec' group or are
		subscribed: {correct_recipients}.
	"""
	print(help_text)

	client.force_login(user)
	client.post(
		reverse(ideas_url),
		{
			"title": idea.title,
			"content": idea.content
		}
	)

	recipients = mail.outbox[0].recipients()
	assert len(recipients) == 3
	assert set(correct_recipients) == set(recipients)


@pytest.mark.django_db
def test_email_has_correct_fields(client, ideas_url, idea, user, email_backend_setup):
	help_text = f"""
		Tests if email is sent with correct fields at: '{ideas_url}'.
		Tested are: 'Subject', 'From', 'Body'.
	"""
	print(help_text)

	user.subscribed = True
	user.save()
	client.force_login(user)
	client.post(
		reverse(ideas_url),
		{
			"title": idea.title,
			"content": idea.content
		}
	)

	email = mail.outbox[0]
	assert "New Idea number" in email.subject
	assert email.from_email == "DjangoApp"
	assert idea.content in email.body


@pytest.mark.django_db
def test_subscribe_form_available_on_ideas_and_profile_page(client, ideas_url, profile_url, user):
	form_id = "subscribe_form"
	help_text = f"""
		Tests if subscribe form is present at endpoints: '{ideas_url}' and '{profile_url}'.
		Tests form (with id = '{form_id}') and button presence.
	"""
	print(help_text)

	user.subscribed = False
	user.save()
	client.force_login(user)
	for url in [ideas_url, profile_url]:
		response = client.get(reverse(url))
		soup = Bs(response.content, 'html.parser')
		form = soup.find(id=form_id)
		assert form
		assert not form.get('hidden')
		assert not form.get('disabled')
		button = form.find('button')
		assert button
		assert not button.get('hidden')
		assert not button.get('disabled')


@pytest.mark.django_db
def test_subscribe_form_changes_user_attributes(client, ideas_url, user):
	help_text = f"""
		Tests if subscribe form changes user's 'subscribed' attribute at: '{ideas_url}'.
	"""
	print(help_text)

	user.subscribed = False
	user.save()
	client.force_login(user)
	client.post(
		reverse(ideas_url),
		{
			"subscribe": True
		}
	)
	updated_user = get_user_model().objects.get(username=user.username)
	assert updated_user.subscribed == True


@pytest.mark.django_db
def test_user_changing_status_affects_email_sending(client, ideas_url, user, idea, email_backend_setup):
	help_text = f"""
		Chained test:
		1) Unsubscribed user doesn't receive email
		2) User subscribes
		3) Subscribed user receives email
		at: '{ideas_url}'
	"""
	print(help_text)

	user.subscribed = False
	user.save()
	client.force_login(user)
	client.post(
		reverse(ideas_url),
		{
			"title": idea.title,
			"content": idea.content
		}
	)
	assert len(mail.outbox) == 0

	client.post(
		reverse(ideas_url),
		{
			"subscribe": True
		}
	)
	client.post(
		reverse(ideas_url),
		{
			"title": idea.title,
			"content": idea.content
		}
	)
	assert len(mail.outbox) == 1


"""Alternative approach with mocker"""
# @pytest.mark.django_db
# def test_send_email_mocker(mocker, idea):
# 	name = 'users.email.send_mail'
# 	recipients = ["a@a.pl", "kajtekbezmajtek@gmail.com"]
#
# 	mock_smtp = mocker.MagicMock(name=name)
# 	mocker.patch(name, new=mock_smtp)
#
# 	send_message(recipients, idea)
