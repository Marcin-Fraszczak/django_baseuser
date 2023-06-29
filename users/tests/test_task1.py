"""
Unit tests for part 1 of the recruitment task (numbers sorting app).

Run command with report creation:
pytest --html=templates/tests/report.html --self-contained-html

"""
from random import shuffle
from django.urls import reverse
from bs4 import BeautifulSoup as Bs


def test_url_exists_at_correct_location(client, home_url):
	manual_url = "/"
	help_text = f"""
	Tests if server responds with status code 200 at endpoint: '{manual_url}'.
	Also checks internal links regarding the same endpoints: '{home_url}'.
	"""
	print(help_text)

	response = client.get(manual_url)
	assert response.status_code == 200
	response = client.get(reverse(home_url))
	assert response.status_code == 200


def test_proper_form_loaded(client, home_url, form_id):
	help_text = f"""
		Tests if proper form (identified by id = '{form_id}') is loaded at location: '{home_url}'.
	"""
	print(help_text)

	response = client.get(reverse(home_url))
	soup = Bs(response.content, 'html.parser')
	form = soup.find(id=form_id)
	assert form
	# a bit naive version checking if the header is present:
	assert "<h2>Numbers sorting form</h2>" in response.content.decode('UTF-8')


def test_input_is_present_correct_type_and_available(client, home_url, form_id, input_id):
	help_text = f"""
		Tests if form (identified by id = '{form_id}') is loaded with a specific
		input element (identified by id = '{input_id}') at location: '{home_url}'.
		Also tests if input has correct type and is not disabled or hidden.
	"""
	print(help_text)

	response = client.get(reverse(home_url))
	soup = Bs(response.content, 'html.parser')
	# chaining is not necessary, but I want to be sure,
	# that input is a part of this specific form:
	input_element = soup.find(id=form_id).find(id=input_id)
	assert input_element
	assert input_element.get("type") == 'text'
	# naive method that doesn't account for styling, only HTML attrs
	# (object can be moved of the window scope):
	assert not input_element.get("hidden")
	assert not input_element.get("disabled")


def test_submit_button_is_present_and_active(client, home_url, form_id):
	help_text = f"""
		Tests if form (identified by id = '{form_id}') is loaded with
		a working button at location: '{home_url}'.
	"""
	print(help_text)

	response = client.get(reverse(home_url))
	soup = Bs(response.content, 'html.parser')
	# again, "submit" doesn't have to be explicitly declared in the form,
	# alternative would be to look just for any button inside the form
	button = soup.find(id=form_id).find(type="submit")
	assert button
	assert button.text == "Sort"
	assert not button.hidden
	assert not button.disabled


def test_warning_displayed_for_request_with_no_input(client, home_url):
	help_text = f"""
		Tests if warning is displayed to the user when form is sent
		with no input at location: '{home_url}'.
	"""
	print(help_text)

	response = client.post(
		reverse(home_url),
		{
			"in_data": ""
		}
	)
	assert response.status_code == 200
	assert "No input!" in response.content.decode('UTF-8')


def test_field_error_displayed_for_empty_required_field(client, home_url):
	help_text = f"""
		Tests if required field gets error message
		when submitted empty at location: '{home_url}'.
	"""
	print(help_text)

	response = client.post(
		reverse(home_url),
		{
			"in_data": ""
		}
	)
	assert response.status_code == 200
	assert "This field is required" in response.content.decode('UTF-8')


def test_warning_displayed_for_incorrect_datatype_posted(client, home_url):
	help_text = f"""
		Tests if warning is displayed when improper data type is passed into a form
		at location: '{home_url}'. Passing string (non digit), digit-character mix, functions (built-ins and custom).
	"""
	print(help_text)

	def func():
		pass

	"""Note, that algorithm will work for collections with digits, but will only consider
	first (dictionaries) or last value from collection (list, tuples, sets).
	Problem is in a way that form-data is sent, not in a algorithm itself."""
	incorrect_data = ["a", "Ala ma kota 34", int, func]
	for data in incorrect_data:
		response = client.post(
			reverse(home_url),
			{
				"in_data": data
			}
		)
		assert response.status_code == 200
		assert "Invalid input!" in response.content.decode('UTF-8')


def test_warning_displayed_for_incorrect_separators_used(client, home_url):
	separators = ["+", "-", ":", ";", "/", ",", ".", "&"]
	help_text = f"""
		Tests if warning is displayed when improper separator is passed into a form
		at location: '{home_url}'. Separators are {separators}.
	"""
	print(help_text)

	"""Space is the correct separator now (multiple spaces allowed).
	Underscore ('_') is allowed as a way to write bigger numbers,
	for example 1_000 equals 1000. Python converts also 1_2 to 12 and 1_2_0 to 120.
	Single plus or minus is also allowed"""
	incorrect_data = [f"2{sep}1{sep}0" for sep in separators]
	for data in incorrect_data:
		response = client.post(
			reverse(home_url),
			{
				"in_data": data
			}
		)
		assert response.status_code == 200
		assert "Invalid input!" in response.content.decode('UTF-8')


def test_results_appear_on_the_page(client, home_url):
	help_text = f"""
		Tests if result is displayed when sending correct data
		at location: '{home_url}'.
	"""
	print(help_text)

	response = client.post(
		reverse(home_url),
		{
			"in_data": "3 2 1"
		}
	)
	soup = Bs(response.content, 'html.parser')
	result_element = soup.find(id="out-data")
	assert result_element
	assert not result_element.get('hidden')


def test_correct_result_is_returned(client, home_url):
	def shuffler(limit):
		result = [str(x) for x in range(limit)]
		shuffle(result)
		return result

	test_data = {
		"1": "1",
		"3 2 1": "1 2 3",
		"9 -2 2000": "-2 9 2000",
		"2.3 0.0001 -40": "-40 0.0001 2.3",
		"+2.3 -1 1_4": "-1 2.3 14",
		" ".join(shuffler(1000)): " ".join((str(x) for x in range(1000))),
	}
	help_text = f"""
		Tests if correct results are returned when sending correct data
		at location: '{home_url}'. Input data is:
		{list(test_data.keys())[:-1]} and a 1000 elements shuffled list.
	"""
	print(help_text)

	for case in test_data:
		response = client.post(
			reverse(home_url),
			{
				"in_data": case
			}
		)
		assert test_data[case] in response.content.decode('UTF-8')
