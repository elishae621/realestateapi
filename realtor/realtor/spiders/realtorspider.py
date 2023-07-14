import scrapy
import environ
import random
import os
import json
from bs4 import BeautifulSoup
from pathlib import Path
from scrapy.crawler import CrawlerProcess
from scrapy_playwright.page import PageMethod

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
    
class RealtorSpider(scrapy.Spider):
    name = "realtor"
    allowed_domains = ["realtor.com"]
    custom_settings={
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "DOWNLOAD_HANDLERS": {
                "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
            "PLAYWRIGHT_PROCESS_REQUEST_HEADERS": custom_headers,
            "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 0,
            "LOG_LEVEL": "DEBUG",
            "ROBOTSTXT_OBEY": False,
            "PLAYWRIGHT_LAUNCH_OPTIONS":{
                "headless": True,
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
    
    def start_requests(self):
        category_dict = {
            'buy': 'realestateandhomes-search',
            'rent': 'apartments'   
        }
        for state in states:
            yield scrapy.Request(f'https://www.realtor.com/{category_dict[self.category]}/{state}/pg-{self.page}',
                headers=headers,
                meta=dict(
                playwright = True,
                playwright_include_page = True,
                playwright_page_coroutines = [
                PageMethod("wait_for_selector", "div.result-list"),
                ]
            ))

    async def parse(self, response):
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            page = response.meta["playwright_page"]
            data = json.loads(soup.css.select('script#__NEXT_DATA__')[0].text)
            try: 
                links = ['https://www.realtor.com/realestateandhomes-detail/{}/'.format(item['permalink']) for item in data['props']['pageProps']['properties']]
            except KeyError:
                links = ['https://www.realtor.com/realestateandhomes-detail{}/'.format(atags.attrs['href']) for atags in soup.css.select('div.result-list li[data-testid="result-card"] a')]
            for link in links:
                yield scrapy.Request(link,
                    headers=headers,
                    meta=dict(
                    playwright = True,
                    playwright_include_page = True,
                ))
        else:
            pass

    async def parse_property(self, response):
        pass 
    
if __name__ == "__main__":
    process = CrawlerProcess()
    for page in range(291, 300):
        for category in ['buy', 'rent']:
            process.crawl("realtor", page=page, category=category)
            process.start()
    print("finished")