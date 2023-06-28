from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

GROUPS = ['No group', "H/Div", "H/Sec", "H/Ple"]
MODELS = ['idea']
PERMISSIONS = ['view', 'add', 'delete']


class Command(BaseCommand):
	help = 'Creates default user groups'

	def handle(self, *args, **options):
		for group in GROUPS:
			new_group, created = Group.objects.get_or_create(name=group)
			for model in MODELS:
				for permission in PERMISSIONS:
					name = f"Can {permission} {model}"
					try:
						model_add_perm = Permission.objects.get(name=name)
					except Permission.DoesNotExist:
						print(f"Permission {name} not found")
						continue
					new_group.permissions.add(model_add_perm)