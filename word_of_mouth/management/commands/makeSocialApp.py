from django.core.management.base import BaseCommand, CommandError
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
import os
os.environ['client_id'] = 'env var SET CLIENT ID HERE'
os.environ['secret_key'] = 'env var SET SECRET KEY HERE'
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'


    def add_arguments(self, parser):
        parser.add_argument("-d", "--delay", type=int)
        #I don't know how to make it not require an argument so this argument will do nothing for now
    def handle(self, *args, **options):
        #our_client_id = 'SET CLIENT ID HERE'    VARIABLES NO LONGER NEEDED
        #secret_key = 'SET SECRET KEY HERE'
        try:
            SocialApp.objects.get(secret=os.environ['secret_key'], client_id=os.environ['client_id'])
            print('Social App already exists')
        except SocialApp.DoesNotExist:
            sapp = SocialApp(provider='google', name='any',
                             client_id=os.environ['client_id'],
                             secret=os.environ['secret_key'])

            sapp.save()
            s = Site.objects.get(id=1)
            s.domain = 'localhost'
            s.save()
            sapp.sites.add(1)
            sapp.save()
            self.stdout.write(self.style.SUCCESS('Successfully made new Social App'))