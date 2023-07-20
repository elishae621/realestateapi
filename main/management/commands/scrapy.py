from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings
import sys
import requests
import os
import environ

env = environ.Env(PRODUCTION=(bool, True))

environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))

current_site = Site.objects.get_current()

scheme = 'https' if env('PRODUCTION') else 'http'
domain = current_site.domain

states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming", "Washington_DC"]

category_dict = {
        'buy': 'realestateandhomes-search',
        'rent': 'apartments'   
    }
class Command(BaseCommand):
    help = 'Custom Django command to run scrapy'

    def handle(self, *args, **options):
        sys.path.insert(0, settings.BASE_DIR)
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'realtor.realtor.settings'
        for category in ['buy', 'rent']:
            for page in range(3, 4):
                for state in states:
                    requests.post(f'{scheme}://{domain}/crawl/', data={'url': f'https://www.realtor.com/{category_dict[category]}/{state}/pg-{page}'})
        self.stdout.write("running scrapy")