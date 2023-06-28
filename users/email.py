from django.core.mail import send_mail, EmailMessage
from os import getenv


def send_message(recipients, idea):

	send_mail(
		subject=f'New Idea number {idea.pk}',
		message=f"""
		This idea was created {idea.created} by {idea.owner.username}.
		It states that:
		
		{idea.content}""",
		from_email='DjangoApp',
		recipient_list=recipients,
		auth_user=getenv('EMAIL_HOST_USER'),
		auth_password=getenv('EMAIL_HOST_PASSWORD'),
		fail_silently=False
	)