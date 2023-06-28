from django.core.exceptions import ValidationError
from re import sub as re_sub


class CustomPasswordValidator:
	def validate(self, password, user=None):
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
			raise ValidationError(errors, code="password_too_weak")

	def get_help_text(self):
		return "Password should have at least one of each: small letter, capital letter, digit, special sign."


def normalize_email(email):
	try:
		# 1.  Trim whitespace from both ends of the address.
		# 2.  Lowercase the address.
		# 3.  Find the local part of the email and the domain.
		email_name, domain_part = email.strip().lower().rsplit("@", 1)
		# 4.  Trim the whitespace from the domain.
		# 5.  Trim any number of periods from the end of the domain.
		domain_part = domain_part.lstrip().rstrip('.')
		# 6.  Convert international domain names to ASCII.
		# domain_part = domain_part.encode("idna")
		# 7.  Check for common typos.
		"""not implemented"""
		# 8.  Remove repetitions of '.com'.
		# 9.  Remove any characters after '.com'.
		re_sub('\.com[a-z0-9]+', '.com', domain_part)
		# 10. Remove leading digits in 'gmail.com'.
		re_sub('[0-9]+gmail.com', 'gmail.com', domain_part)
		# 11. For fastmail.com replace the email local part with the subdomain.
		"""not implemented"""
		# 12. Remove alias parts from the local part.
		"""not implemented"""
		# 13. Put the local part and the domain part back together.
		email = f"{email_name}@{domain_part}"
		# 14. Calculate the MD5 hash.
		"""not implemented"""
		return email
	except ValueError:
		return ""
