from django.core.management.base import BaseCommand
from realtor.realtor.spiders.realtorspider import scrape

class Command(BaseCommand):
    help = 'Custom Django command to run scrapy'

    def handle(self, *args, **options):
        scrape()
        self.stdout.write("running scrapy")