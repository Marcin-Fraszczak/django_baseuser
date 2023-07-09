"""
Unit tests for registration functionality.
"""
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from bs4 import BeautifulSoup as Bs


@pytest.mark.skip(reason="too much")
def test_url_exists_at_correct_location(client, register_url):
	manual_url = "/users/register/"
	help_text = f"""
		Tests if server responds with status code 200 at endpoint: '{manual_url}'.
		Also checks internal links regarding the same endpoints: '{register_url}'.
		"""
	print(help_text)

	response = client.get(manual_url)
	assert response.status_code == 200
	response = client.get(reverse(register_url))
	assert response.status_code == 200


@pytest.mark.skip(reason="too much")
def test_proper_template_loaded(client, register_url):
	proper_templates = ["_base.html", "_navigation.html", "users/register.html"]
	help_text = f"""
		Tests if proper set of templates is loaded at: '{register_url}'.
		Proper set of templates is: {proper_templates}
		"""
	print(help_text)

	response = client.get(reverse(register_url))
	loaded_templates = [temp.name for temp in response.templates]
	for template in proper_templates:
		assert template in loaded_templates


@pytest.mark.skip(reason="too much")
def test_proper_form_is_loaded(client, register_url):
	form_id = "registration_form"
	help_text = f"""
		Tests if proper form is loaded. Form should have id={form_id}.
		"""
	print(help_text)

	response = client.get(reverse(register_url))
	soup = Bs(response.content, 'html.parser')
	form = soup.find(id=form_id)
	assert form
	print(f"OK: Form with id={form_id} is loaded.")


@pytest.mark.skip(reason="too much")
def test_form_has_proper_fields(register_form):
	help_text = f"""
		Tests if registration form has proper field names and types.
		"""
	print(help_text)

	input_fields = {
		"username": "email",
		"password": "password",
	}
	select_field_name = "group"

	for f_name, f_type in input_fields.items():
		field = register_form.find(attrs={"name": f"{f_name}"})
		assert field
		assert field.get('type') == f_type
		assert not field.get("hidden")
		assert not field.get("disabled")
		print(f"OK: Field with name: '{f_name}' exists, has type: '{f_type}' and is available.")
	select_field = register_form.find(attrs={"name": f"{select_field_name}"})
	assert select_field
	assert not select_field.get("hidden")
	assert not select_field.get("disabled")
	print(f"OK: Select field with name: '{select_field_name}' exists and is available.")


@pytest.mark.skip(reason="too much")
def test_form_has_working_submit_button(register_form):
	help_text = f"""
			Tests if registration form has an active submit button.
			"""
	print(help_text)

	button = register_form.find(type='submit')
	assert button
	assert button.name in ['button', 'input']
	assert not button.get("hidden")
	assert not button.get("disabled")
	print("OK: Registration form has active submit button.")


@pytest.mark.skip(reason="too much")
@pytest.mark.django_db
def test_error_message_displayed_when_submitting_empty_form(client, register_url, no_input):
	help_text = f"""
			Tests if registration form displays error messages when submitted empty.
			Proper error message should be: '{no_input}'
			"""
	print(help_text)

	response = client.post(
		reverse(register_url),
		{
			"username": "",
			"password": "",
			"group": "",
		}
	)

	assert response.content.decode('utf-8').count(no_input) == 3
	print(f"OK: All required fields get field error message.")
	assert len(get_user_model().objects.all()) == 0
	print(f"OK: No user created.")

