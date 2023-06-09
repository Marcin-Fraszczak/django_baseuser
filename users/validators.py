from django.core.exceptions import ValidationError


def custom_password_validator(password):
	ascii_specials = tuple(range(33, 48)) + tuple(range(58, 65)) + tuple(range(91, 97)) + tuple(range(123, 126))
	specials = [chr(i) for i in ascii_specials]
	min_length = 10
	max_length = 64
	errors = []
	# min length validation
	if len(password) < min_length:
		errors.append(f"Password should have at least {min_length} characters.")
	# max length validator
	if len(password) > max_length:
		errors.append(f"Password should have no more than {max_length} characters.")
	# small letter present validation
	if not (char for char in password if char.islower()):
		errors.append("Password should have at least 1 lower case letter.")
	# capital letter present validation
	if not [char for char in password if char.isupper()]:
		errors.append("Password should have at least 1 upper case letter.")
	# number present validation
	if not [char for char in password if char.isdigit()]:
		errors.append("Password should have at least 1 digit.")
	# special sign present validation
	if not [char for char in password if char in specials]:
		errors.append("Password should have at least 1 special sign.")
	if errors:
		raise ValidationError(errors)


def password_email_similarity_validator(password, email):
	if email.split("@")[0].lower() in password.lower():
		raise ValidationError("Password too similar to other user data.")
