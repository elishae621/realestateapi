from django.core.management.base import BaseCommand
from scrapy import cmdline
from django.conf import settings
import sys
import os
class Command(BaseCommand):
    help = 'Custom Django command to run scrapy'

    def handle(self, *args, **options):
        sys.path.insert(0, settings.BASE_DIR)
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'realtor.realtor.settings'
        cmdline.execute("scrapy crawl realtorspider".split())
        self.stdout.write("running scrapy")