import scrapy
import environ
import random
import os
import logging
import json
import scrapy
from bs4 import BeautifulSoup
from pathlib import Path
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from dateutil.parser import parse
from multiprocessing import Process, Queue
from twisted.internet import reactor
from decimal import Decimal
import django
django.setup()
from main import models

# import sys
# from importlib import import_module

# sys.path.append('main')
# models = import_module('models')


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming", "Washington, DC"]

userAgentStrings = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.3497.92 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
]
headers = {
    'User-Agent': random.choice(userAgentStrings),
}

def custom_headers(browser_type, playwright_request, scrapy_headers):
    return headers

def extract(value):
    return value if value else None
class RealtorspiderSpider(scrapy.Spider):
    name = "realtorspider"
    allowed_domains = ["realtor.com"]
    custom_settings={
            "DOWNLOAD_HANDLERS": {
                "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
            "PLAYWRIGHT_PROCESS_REQUEST_HEADERS": custom_headers,
            "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 0,
            "LOG_LEVEL": "INFO",
            "ROBOTSTXT_OBEY": False,
            "PLAYWRIGHT_LAUNCH_OPTIONS":{
                "headless": False,
                "channel": "chrome",
            },
            "PLAYWRIGHT_CONTEXTS": {
                "default": {
                    "viewport": {
                        "width": 1920,
                        "height": 1080,
                    },
                }
            },
        }
    if __name__ == '__main__':
        custom_settings["TWISTED_REACTOR"] = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
    else:
        custom_settings["TWISTED_REACTOR"] = "twisted.internet.selectreactor.SelectReactor"
    
    def start_requests(self):
        category_dict = {
            'buy': 'realestateandhomes-search',
            'rent': 'apartments'   
        }
        # https://www.realtor.com/realestateandhomes-detail/7309-Azimuth-Ln_Sacramento_CA_95842_M29288-48779
        link = 'https://www.realtor.com/realestateandhomes-detail/12475-State-Highway-180-Lot-37_Gulf-Shores_AL_36542_M93923-36924/'
        self.logger.info('in property link = {}'.format(link))
        yield scrapy.Request(link,
            headers=headers,
            callback=self.parse_property,
            meta=dict(
            playwright = True,
            playwright_include_page = True,
        ))
        # for state in states:
        # for state in ['Alabama']:
        #     url = f'https://www.realtor.com/{category_dict[self.category]}/{state}/pg-{self.page}'
        #     self.logger.info('in url = {}'.format(url))
        #     yield scrapy.Request(url,
        #         headers=headers,
        #         callback=self.parse_state,
        #         meta=dict(
        #         playwright = True,
        #         playwright_include_page = True,
        #         playwright_page_coroutines = [
        #         PageMethod("wait_for_selector", "div.result-list"),
        #         ]
        #     ))

    async def parse_state(self, response):
        self.logger.info("Parse state function called on %s", response.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        page = response.meta["playwright_page"]
        data = json.loads(soup.css.select('script#__NEXT_DATA__')[0].text)
        try: 
            links = ['https://www.realtor.com/realestateandhomes-detail/{}/'.format(item['permalink']) for item in data['props']['pageProps']['properties']]
        except KeyError:
            try:
                links = ['https://www.realtor.com{}/'.format(atags.attrs['href']) for atags in soup.css.select('div.result-list li[data-testid="result-card"] a')]
            except KeyError:
                pass
            
        for link in links:
            self.logger.info('in property link = {}'.format(link))
            yield scrapy.Request(link,
                headers=headers,
                callback=self.parse_property,
                meta=dict(
                playwright = True,
                playwright_include_page = True,
            ))

    

    async def parse_property(self, response):
        self.logger.info("Parse property function called on %s", response.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = json.loads(soup.css.select('script#__NEXT_DATA__')[0].text)['props']['pageProps']['property']
        if len(data['local'] > 1):
            pass
        if data['community']:
            pass
        if data['matterport']:
            pass
        if data['floorplans']['floorplan_2d']:
            pass
        if data['open_houses']:
            pass
        if data['tax_history']:
            pass
        if data['hoa']:
            pass
        if data['location']['neighborhoods']:
            pass
        if data['videos']:
            pass
        if data['unit_count'] or data['units']:
            pass
        if data['neighborhood'] or data['nearby_neighborhoods']:
            pass
        property = models.Property.objects.create(
            flood_factor_score=extract(data['local']['flood']['flood_factor_score']),
            flood_fema_zone=extract(data['local']['flood']['femazone'][0]),
            move_in_date=extract(data['move_in_date']),
            status=extract(data['for_sale']),
            coming_soon_date=extract(data['coming_soon_date']),
            source_url=extract(data['href']),
            list_price=extract(data['list_price']),
            last_price_change_amount=extract(data['last_price_change_amount']),
            list_price_min=extract(data['list_price_min']),
            list_price_max=extract(data['list_price_max']),
            price_per_sqft=extract(data['price_per_sqft']),
            list_date=extract(data['list_date']),
            address=extract(data['location']['address']),
            street_number=extract(data['location']['street_number']),
            street_direction=extract(data['location']['street_direction']),
            street_name=extract(data['location']['street_name']),
            street_suffix=extract(data['location']['street_suffix']),
            street_post_direction=extract(data['location']['street_post_direction']),
            unit=extract(data['location']['unit']),
            city=extract(data['location']['city']),
            state_code=extract(data['location']['state_code']),
            postal_code=extract(data['location']['postal_code']),
            country=extract(data['location']['country']),
            validation_code=extract(data['location']['validation_code']),
            state=extract(data['location']['state']),
            latitude=Decimal(extract(data['location']['lat'])),
            longitude=Decimal(extract(data['location']['lon'])),
            cross_street=extract(data['location']['cross_street']),
            driving_directions=extract(data['location']['driving_directions']),
            builder=extract(data['builder']),
            baths=extract(data['description']['baths']),
            baths_consolidated=extract(data['description']['baths_consolidated']),
            baths_full=extract(data['description']['baths_full']),
            baths_3qtr=extract(data['description']['baths_3qtr']),
            baths_half=extract(data['description']['baths_half']),
            baths_1qtr=extract(data['description']['baths_1qtr']),
            baths_min=extract(data['description']['baths_min']),
            baths_max=extract(data['description']['baths_max']),
            beds_min=extract(data['description']['beds_min']),
            beds_max=extract(data['description']['beds_max']),
            beds=extract(data['description']['beds']),
            pool=extract(data['description']['pool']),
            sqft=extract(data['description']['sqft']),
            sqft_min=extract(data['description']['sqft_min']),
            sqft_max=extract(data['description']['sqft_max']),
            lot_sqft=extract(data['description']['lot_sqft']),
            rooms=extract(data['description']['rooms']),
            stories=extract(data['description']['stories']),
            sub_type=extract(data['description']['sub_type']),
            text=extract(data['description']['text']),
            type=extract(data['description']['type']),
            units=extract(data['description']['units']),
            unit_type=extract(data['description']['unit_type']),
            year_built=extract(data['description']['year_built']),
            name=extract(data['description']['name']),
        )
        for photo in data['photos']:
            image = models.Image.objects.create(
                property=property,
                image=photo['href'].replace('.jpg', '-w480_h360_x2.jpg')
            )
            for tag in photo['tags']:
                models.ImageTag.objects.create(
                    image=image,
                    label=tag['label'],
                    probability=tag['probability']
                )
            
        for detail in data['details']:
            if detail['category'] == "Waterfront and Water Access": 
                for item in data['details']['text']:
                    property.waterfront_water_access.add(models.ListItem.objects.create(name=extract(item)))
                    property.save()
            if detail['category'] == "Land Info": 
                for item in data['details']['text']:
                    property.land_info.add(models.ListItem.objects.create(name=extract(item)))
                    property.save()
            if detail['category'] == "School Information": 
                for item in data['details']['text']:
                    property.school_information.add(models.ListItem.objects.create(name=extract(item)))
                    property.save()
            if detail['category'] == "Homeowners Association": 
                for item in data['details']['text']:
                    property.hoa.add(models.ListItem.objects.create(name=extract(item)))
                    property.save()
            if detail['category'] == "Other Property Info": 
                for item in data['details']['text']:
                    property.other_property_info.add(models.ListItem.objects.create(name=extract(item)))
                    property.save()
            if detail['category'] == "Utilities": 
                for item in data['details']['text']:
                    property.utilities.add(models.ListItem.objects.create(name=extract(item)))
                    property.save()
        for history in data['property_history']:
            models.PriceHistory.objects.create(
                date=parse(history['date']),
                event=extract(history['event_name']),
                price=extract(history['price']),
                source=extract(history['source_name']),
                price_sqft=extract(history['price_sqft']),
                property=property
            )
        for tax in data['tax_history']:
            models.TaxHistory.objects.create(
                year=parse(tax['year']),
                taxes=extract(tax['taxes']),
                land=extract(tax['land']),
                additions=extract(tax['additions']),
                total=extract(tax['total']),
                property=property
            )
        for tag in data['tags']:
            property.tags.add(models.ListItem.objects.create(name=extract(tag)))
            property.save()
        models.Flags.objects.create(
            property=property,
            is_pending=extract(data['is_pending']),
            is_contingent=extract(data['is_contingent']),
            is_new_listing=extract(data['is_new_listing']),
            is_new_construction=extract(data['is_new_construction']),
            is_short_sale=extract(data['is_short_sale']),
            is_foreclosure=extract(data['is_foreclosure']),
            is_price_reduced=extract(data['is_price_reduced']),
            is_senior_community=extract(data['is_senior_community']),
            is_deal_available=extract(data['is_deal_available']),
            is_price_excludes_land=extract(data['is_price_excludes_land']),
            is_subdivision=extract(data['is_subdivision']),
            is_coming_soon=extract(data['is_coming_soon']),    
        )
        for advertiser in data['consumer_advertisers']:
            if advertiser['type'] == 'Agent':
                models.Agent.objects.create(
                    property=property,
                    agent_id=advertiser['agent_id'],
                )
                self.logger.info('in agent link = {}'.format(advertiser['href']))
                yield scrapy.Request(f"https://www.realtor.com{advertiser['href']}",
                headers=headers,
                callback=self.parse_agent,
                meta=dict(
                playwright = True,
                playwright_include_page = True,
            ))
        
        pass 
    
    async def parse_agent(self, response):
        self.logger.info("Parse agent function called on %s", response.url)
        self.logger.info("Parse property function called on %s", response.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = json.loads(soup.css.select('script#__NEXT_DATA__')[0].text)['props']['pageProps']
        # agent = models.Agent.objects.get(agent_id=agent_id)
        

def f(q, spider, page, category):
    try:
        settings = get_project_settings()
        runner = CrawlerRunner(settings)
        deferred = runner.crawl(spider, page=page, category=category)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)
            
def run_spider(spider, page, category):
    q = Queue()
    p = Process(target=f, args=(q,spider,page,category))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result
    
def scrape():
    if __name__ == "__main__":
        process = CrawlerProcess()
        for page in range(1, 300):
            for category in ['buy', 'rent']:
                logging.info('starting')
                process.crawl(RealtorspiderSpider, page=page, category=category)
                process.start()
        logging.info("finished")    
    else:
        for page in range(1, 300):
            for category in ['buy', 'rent']:
                logging.info('starting')
                configure_logging()
                run_spider(RealtorspiderSpider, page=page, category=category)
        logging.info("finished")
        