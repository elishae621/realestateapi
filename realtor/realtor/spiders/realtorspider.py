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
        url = "https://www.realtor.com/realestateandhomes-detail/7309-Azimuth-Ln_Sacramento_CA_95842_M29288-48779"
        # url = 'https://www.realtor.com/realestateandhomes-detail/1511-A-St-NE-Apt-1_Washington_DC_20002_M96274-98187'
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
                headers=headers, 
                meta=meta)
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
            
        for link in links:
            self.logger.info('in property link = {}'.format(link))
        yield scrapy.Request(link,
            headers=headers, meta=meta)


    def parse(self, response):
        self.logger.info("Parse property function called on %s", response.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print("url", response.url)
        try:
            item = json.loads(soup.css.select('script#__NEXT_DATA__')[0].text)['props']['pageProps']['property']
        except:
            item = json.loads(soup.css.select('script#__NEXT_DATA__')[0].text)['props']['pageProps']['initialReduxState']['propertyDetails']
        
        data = {}
        data['property'] = item
        
        for advertiser in item['consumer_advertisers']:
            if advertiser['type'] == 'Agent':
                self.logger.info('in agent link = {}'.format(advertiser['href']))
                yield scrapy.Request(f"https://www.realtor.com{advertiser['href']}",
                headers=headers,
                callback=self.parse_agent, meta={'data': data}
                )
                
        yield data
    
    def parse_agent(self, response):
        self.logger.info("Parse agent function called on %s", response.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        item = json.loads(soup.css.select('script#__NEXT_DATA__')[0].text)['props']['pageProps']['agentDetails']
        data = response.meta['data']
        data['agent'] = item
        return data
        
if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(RealtorspiderSpider)
    process.start()