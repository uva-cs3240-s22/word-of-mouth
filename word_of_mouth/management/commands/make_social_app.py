from django.core.management.base import BaseCommand, CommandError
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from dotenv import load_dotenv

import os
load_dotenv()
class Command(BaseCommand):
    help = 'Makes a new social app using environment variables.'

    def handle(self, *args, **options):
        try:

            our_client_id = os.getenv('GOOGLE_CLIENT_ID')
            secret_key = os.getenv('GOOGLE_SECRET_KEY')

            SocialApp.objects.get(secret=secret_key, client_id=our_client_id)
            print('Social App already exists')
        except SocialApp.DoesNotExist:
            sapp = SocialApp(provider='google', name='any',
                             client_id=our_client_id,
                             secret=secret_key)

            sapp.save()
            s = Site.objects.get(id=1)
            s.domain = 'localhost'
            s.save()
            sapp.sites.add(1)
            sapp.save()
            self.stdout.write(self.style.SUCCESS('Successfully made new Social App'))

