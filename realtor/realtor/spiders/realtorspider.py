import scrapy
import random
import logging
import time
import json
import scrapy
import os
import sys
import environ
from bs4 import BeautifulSoup
from pathlib import Path
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from multiprocessing import Process, Queue
from scrapy_playwright.page import PageMethod
sys.path.append(os.path.dirname(os.path.abspath('./main')))
from main import models
from dateutil.parser import parse
from decimal import Decimal

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(BASE_DIR)

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

meta = {}
    
def extract(item, filters, date=False, image=False, decimal=False):
    filters_list = filters.split(",")
    value = item
    try:
        while filters_list and value:
            value = value[filters_list[0]]
            filters_list.pop(0)
    except KeyError:
        return None
    if image:
        item['href'].replace('.jpg', '-w480_h360_x2.jpg')
    if value and decimal:
        value = Decimal(value)
    if value and date:
        value = parse(value)
    return value

states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming", "Washington_DC"]

userAgentStrings = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.3497.92 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]
headers = {
    'User-Agent': random.choice(userAgentStrings),
}

def custom_headers(browser_type, playwright_request, scrapy_headers):
    return headers

class RealtorspiderSpider(scrapy.Spider):
    name = "realtorspider"
    allowed_domains = ["realtor.com", "localhost"]
    custom_settings = get_project_settings()
    
    def start_requests(self):
        category_dict = {
            'buy': 'realestateandhomes-search',
            'rent': 'apartments'   
        }
        # https://www.realtor.com/realestateandhomes-detail/7309-Azimuth-Ln_Sacramento_CA_95842_M29288-48779
        url = 'https://www.realtor.com/realestateandhomes-detail/1511-A-St-NE-Apt-1_Washington_DC_20002_M96274-98187'
        # url = "https://www.realtor.com/realestateagents/Tumi-Demuren_Washington_DC_1556450"
        # for state in states:
        # for state in ['Alabama']:
        # category = 'rent'
        # page = random.randint(1, 5)
        # state = random.choice(states).replace(' ', '-')
        # url = f'https://www.realtor.com/{category_dict[category]}/{state}/pg-{page}'
        if 'realestateandhomes-detail' in url:
            self.logger.info('in property link = {}'.format(url))
            yield scrapy.Request(url,
                headers=headers, meta=meta)
        elif 'realestateagents' in url:
            self.logger.info('in agent page = {}'.format(url))
            yield scrapy.Request(url,
                callback=self.parse_agent,
                headers=headers, meta=meta)
        else:
            self.logger.info('in state url = {}'.format(url))
            yield scrapy.Request(url,
                headers=headers,
                callback=self.parse_state,
                meta=dict(
                playwright = True,
                playwright_include_page = True,
                playwright_page_coroutines = [
                PageMethod("wait_for_selector", "div.result-list"),
                ]
            ))

    def parse_state(self, response):
        self.logger.info("Parse state function called on %s", response.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = json.loads(soup.css.select('script#__NEXT_DATA__')[0].text)
        try: 
            links = ['https://www.realtor.com/realestateandhomes-detail/{}/'.format(item['permalink']) for item in data['props']['pageProps']['properties']]
        except KeyError:
            try:
                links = ['https://www.realtor.com{}/'.format(atags.attrs['href']) for atags in soup.css.select('div.result-list li[data-testid="result-card"] a')]
            except KeyError:
                pass
            
        # for link in links:
        self.logger.info('in property link = {}'.format(links[5]))
        yield scrapy.Request(links[5],
            headers=headers, meta=meta)


    def parse(self, response):
        self.logger.info("Parse property function called on %s", response.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            item = json.loads(soup.css.select('script#__NEXT_DATA__')[0].text)['props']['pageProps']['property']
        except:
            item = json.loads(soup.css.select('script#__NEXT_DATA__')[0].text)['props']['pageProps']['initialReduxState']['propertyDetails']
        property = models.Property.objects.create(
            flood_factor_severity=extract(item, 'local,flood,flood_factor_severity'),
            flood_trend=extract(item, 'local,flood,flood_trend'),
            fire_factor_severity=extract(item, 'local,wildfire,fire_factor_severity'),
            fire_trend=extract(item, 'local,wildfire,fire_trend'),
            status=extract(item, 'status'),
            coming_soon_date=extract(item, 'coming_soon_date', date=True),
            source_url=extract(item, 'href'),
            list_price=extract(item, 'list_price'),
            last_price_change_amount=extract(item, 'last_price_change_amount'),
            last_sold_date=extract(item, 'last_sold_date', date=True),
            last_sold_price=extract(item, 'last_sold_price'),
            price_per_sqft=extract(item, 'price_per_sqft'),
            list_date=extract(item, 'list_date', date=True),
            address=extract(item, 'location,address,line'),
            street_view_url=extract(item, 'location,address,street_view_url'),
            street_view_metadata_url=extract(item, 'location,address,street_view_metadata_url'),
            street_number=extract(item, 'location,address,street_number'),
            street_direction=extract(item, 'location,address,street_direction'),
            street_name=extract(item, 'location,address,street_name'),
            street_suffix=extract(item, 'location,address,street_suffix'),
            street_post_direction=extract(item, 'location,address,street_post_direction'),
            unit=extract(item, 'location,address,unit'),
            county=extract(item, 'location,county,name'),
            city=extract(item, 'location,address,city'),
            state_code=extract(item, 'location,address,state_code'),
            postal_code=extract(item, 'location,address,postal_code'),
            country=extract(item, 'location,address,country'),
            validation_code=extract(item, 'location,address,validation_code'),
            state=extract(item, 'location,address,state'),
            latitude=extract(item, 'location,address,coordinate,lat', decimal=True),
            longitude=extract(item, 'location,address,coordinate,lon', decimal=True),
            driving_directions=extract(item, 'location,driving_directions'),
            builder=extract(item, 'builder'),
            baths=extract(item, 'description,baths'),
            baths_consolidated=extract(item, 'description,baths_consolidated'),
            baths_full=extract(item, 'description,baths_full'),
            baths_3qtr=extract(item, 'description,baths_3qtr'),
            baths_half=extract(item, 'description,baths_half'),
            baths_total=extract(item, 'description,baths_total'),
            beds=extract(item, 'description,beds'),
            construction=extract(item, 'description,construction'),
            cooling=extract(item, 'description,cooling'),
            exterior=extract(item, 'description,exterior'),
            fireplace=extract(item, 'description,fireplace'),
            garage=extract(item, 'description,garage'),
            garage_type=extract(item, 'description,garage_type'),
            heating=extract(item, 'description,heating'),
            roofing=extract(item, 'description,roofing'),
            pool=extract(item, 'description,pool'),
            sqft=extract(item, 'description,sqft'),
            lot_sqft=extract(item, 'description,lot_sqft'),
            rooms=extract(item, 'description,rooms'),
            stories=extract(item, 'description,stories'),
            sub_type=extract(item, 'description,sub_type'),
            text=extract(item, 'description,text'),
            type=extract(item, 'description,type'),
            units=extract(item, 'description,units'),
            year_built=extract(item, 'description,year_built'),
            year_renovated=extract(item, 'description,year_renovated'),
            zoning=extract(item, 'description,zoning'),
            name=extract(item, 'description,name'),
            primary_photo=extract(item, 'primary_photo,href', image=True)
        )
        for photo in item['photos']:
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
            
        for detail in item['details']:
            if detail['category'] == "Waterfront and Water Access": 
                for item in item['details']['text']:
                    property.waterfront_water_access.add(models.ListItem.objects.create(name=extract(item)))
                    property.save()
            if detail['category'] == "Land Info": 
                for item in item['details']['text']:
                    property.land_info.add(models.ListItem.objects.create(name=extract(item)))
                    property.save()
            if detail['category'] == "School Information": 
                for item in item['details']['text']:
                    property.school_information.add(models.ListItem.objects.create(name=extract(item)))
                    property.save()
            if detail['category'] == "Homeowners Association": 
                for item in item['details']['text']:
                    property.hoa.add(models.ListItem.objects.create(name=extract(item)))
                    property.save()
            if detail['category'] == "Other Property Info": 
                for item in item['details']['text']:
                    property.other_property_info.add(models.ListItem.objects.create(name=extract(item)))
                    property.save()
            if detail['category'] == "Utilities": 
                for item in item['details']['text']:
                    property.utilities.add(models.ListItem.objects.create(name=extract(item)))
                    property.save()
        for history in item['property_history']:
            models.PriceHistory.objects.create(
                date=parse(history, 'date'),
                event=extract(history, 'event_name'),
                price=extract(history, 'price'),
                source=extract(history, 'source_name'),
                price_sqft=extract(history, 'price_sqft'),
                property=property
            )
        for tax in item['tax_history']:
            models.TaxHistory.objects.create(
                year=extract(tax, 'year'),
                taxes=extract(tax, 'taxes'),
                land=extract(tax, 'land'),
                additions=extract(tax, 'additions'),
                total=extract(tax, 'total'),
                property=property
            )
            
        if item['neighborhood']:
            neighborhood, created = models.Neighborhood.objects.get_or_create(local_url=extract(item, 'neighborhood,local_url'))
            models.Neighborhood.objects.filter(local_url=neighborhood.local_url).update(
                area=extract(item, 'neighborhood,area'),
                median_price_per_sqft=extract(item, 'neighborhood,median_price_per_sqft'),
                median_listing_price=extract(item, 'neighborhood,median_listing_price'),
                median_sold_price=extract(item, 'neighborhood,median_sold_price'),
                median_days_on_market=extract(item, 'neighborhood,median_days_on_market'),
                hot_market_badge=extract(item, 'neighborhood,hot_market_badge'),
            )
        
            for nbh in item['nearby_neighborhood']:
                nearby_nbh, created = models.Neighborhood.objects.get_or_create(local_url=extract(nbh, 'local_url'))
                models.Neighborhood.objects.filter(local_url=nearby_nbh.local_url).update(
                    area=extract(nbh, 'area'),
                    median_listing_price=extract(nbh, 'median_listing_price'),
                )
                
                neighborhood.nearby_neighborhoods.add(nearby_nbh)
                neighborhood.save()

            
        for school in item['school']:
            sch = models.School.objects.create(
                longitude=extract(school, 'coordinate,lon', decimal=True),
                latitude=extract(school, 'coordinate,lat', decimal=True),
                distance_in_miles=extract(school, 'distance_in_miles'),
                district=extract(school, 'district,name'),
                funding_type=extract(school, 'funding_type'),
                greatschools_id=extract(school, 'greatschools_id'),
                name=extract(school, 'name'),
                nces_code=extract(school, 'nces_code'),
                parent_rating=extract(school, 'parent_rating'),
                review_count=extract(school, 'review_count'),
                student_count=extract(school, 'student_count'),
            )
            for level in school['education_levels']:
                sch.education_levels.add(models.ListItem.objects.create(name=level))
                sch.save()
                
            for grade in school['grades']:
                sch.grades.add(models.ListItem.objects.create(name=grade))
                sch.save()
            
            property.schools.add(sch)
            property.save()
            
        for tag in item['tags']:
            property.tags.add(models.ListItem.objects.create(name=extract(tag)))
            property.save()
        models.Flags.objects.create(
            property=property,
            is_pending=extract(item, 'flags,is_pending'),
            is_contingent=extract(item, 'flags,is_contingent'),
            is_new_listing=extract(item, 'flags,is_new_listing'),
            is_new_construction=extract(item, 'flags,is_new_construction'),
            is_short_sale=extract(item, 'flags,is_short_sale'),
            is_foreclosure=extract(item, 'flags,is_foreclosure'),
            is_price_reduced=extract(item, 'flags,is_price_reduced'),
            is_senior_community=extract(item, 'flags,is_senior_community'),
            is_deal_available=extract(item, 'flags,is_deal_available'),
            is_for_rent=extract(item, 'flags,is_for_rent'),
            is_garage_present=extract(item, 'flags,is_garage_present'),
            is_price_excludes_land=extract(item, 'flags,is_price_excludes_land'),
            is_subdivision=extract(item, 'flags,is_subdivision'),
            is_coming_soon=extract(item, 'flags,is_coming_soon'),    
        )
        
        
        for advertiser in item['consumer_advertisers']:
            if advertiser['type'] == 'Agent':
                agent, created = models.Agent.objects.get_or_create(
                    agent_id=advertiser['agent_id'],
                )
                property.agent = agent
                property.save()
                self.logger.info('in agent link = {}'.format(advertiser['href']))
                yield scrapy.Request(f"https://www.realtor.com{advertiser['href']}",
                headers=headers,
                callback=self.parse_agent, meta=meta
                )
                
        return item
    
    def parse_agent(self, response):
        self.logger.info("Parse agent function called on %s", response.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = json.loads(soup.css.select('script#__NEXT_DATA__')[0].text)['props']['pageProps']['agentDetails']
        agent, created = models.Agent.objects.get_or_create(agent_id=data['advertiser_id'])
        models.Agent.objects.filter(agent_id=data['advertiser_id']).update(
            broker_address=extract(data, 'office,address,line'),
            city=extract(data, 'office,address,city'),
            postal_code=extract(data, 'office,address,postal_code'),
            state_code=extract(data, 'office,address,state_code'),
            country=extract(data, 'office,address,country'),
            broker=extract(data, 'broker,name'),
            description=extract(data, 'description'),
            website=extract(data, 'href'),
            name=extract(data, 'name'),
            last_updated=extract(data, 'last_updated', date=True),
        )
        
        for area in data['served_areas']:
            models.ServedAreas.objects.create(
                name=extract(area, 'name'),
                state_code=extract(area, 'state_code'),
                agent=agent,
            )
            
        for specialization in data['specializations']:
            agent.specializations.add(models.ListItem.objects.create(name=specialization['name']))
            agent.save()

        for phone in data['phones']:
            agent.phones.add(models.ListItem.objects.create(name=phone['number']))
            agent.save()
        pass
        
if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(RealtorspiderSpider)
    process.start()