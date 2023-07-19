import scrapy
import random
import json
import scrapy
import os
import sys
import environ
from bs4 import BeautifulSoup
from pathlib import Path
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy_playwright.page import PageMethod
sys.path.append(os.path.dirname(os.path.abspath('./main')))


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(BASE_DIR)

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

meta = {}


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
        if 'realestateandhomes-detail' in self.url:
            self.logger.info('in property link = {}'.format(self.url))
            yield scrapy.Request(self.url,
                headers=headers, 
                meta=meta)
        elif 'realestateagents' in self.url:
            self.logger.info('in agent page = {}'.format(self.url))
            yield scrapy.Request(self.url,
                callback=self.parse_agent,
                headers=headers, meta=meta)
        else:
            self.logger.info('in state self.url = {}'.format(self.url))
            yield scrapy.Request(self.url,
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
        try:
            item = json.loads(soup.css.select('script#__NEXT_DATA__')[0].text)['props']['pageProps']['property']
        except:
            item = json.loads(soup.css.select('script#__NEXT_DATA__')[0].text)['props']['pageProps']['initialReduxState']['propertyDetails']
        
        data = {}
        data['property'] = item
        
        for advertiser in item['consumer_advertisers']:
            if advertiser['type'] == 'Agent' and advertiser['href']:
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
        yield data
        
if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(RealtorspiderSpider)
    process.start()
