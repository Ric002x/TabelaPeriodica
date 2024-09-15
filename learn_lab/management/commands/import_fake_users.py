import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

load_dotenv()

users = {
    '1': {
        'username': 'David',
        'password': os.getenv('USERPASSWORD')
    },
    '2': {
        'username': 'Alice',
        'password': os.getenv('USERPASSWORD')
    },
    '3': {
        'username': 'Bob',
        'password': os.getenv('USERPASSWORD')
    },
    '4': {
        'username': 'Charlie',
        'password': os.getenv('USERPASSWORD')
    },
    '5': {
        'username': 'Barbara',
        'password': os.getenv('USERPASSWORD')
    },
}


class Command(BaseCommand):
    help = 'import fictinal users'

    def handle(self, *args, **kwargs):
        users_created = 0
        for key, value in users.items():
            if not User.objects.filter(username=value['username']).exists():
                user = User(
                    username=value['username'],
                )
                user.set_password(value['password'])
                user.save()
                users_created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {users_created} users'))
