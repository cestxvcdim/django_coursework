import os

from django.core.management import BaseCommand
from dotenv import load_dotenv

from users.models import User

load_dotenv()


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv('CSU_EMAIL'),
            first_name=os.getenv('CSU_FIRST_NAME'),
            last_name=os.getenv('CSU_LAST_NAME'),
            is_staff=True,
            is_superuser=True,
        )

        user.set_password(os.getenv('CSU_PASSWORD'))
        user.save()
