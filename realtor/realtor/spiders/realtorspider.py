import scrapy
import environ
import random
import os
import json
import html_to_json
from bs4 import BeautifulSoup
from pathlib import Path
from scrapy.crawler import CrawlerProcess
from scrapy_playwright.page import PageMethod

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

def custom_headers(browser_type, playwright_request, scrapy_headers):
    userAgentStrings = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.2228.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.3497.92 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    ]
    return {
        'User-Agent': random.choice(userAgentStrings),
    }
    
class RealtorspiderSpider(scrapy.Spider):
    name = "realtorspider"
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
        url = 'https://www.realtor.com/realestateandhomes-search/Alabama/'
        userAgentStrings = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.2227.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.3497.92 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        ]
        headers = {
            'User-Agent': random.choice(userAgentStrings),
        }
        
        yield scrapy.Request(url,
                             headers=headers,
                             meta=dict(
            playwright = True,
            playwright_include_page = True,
        ))

    async def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        page = response.meta["playwright_page"]
        data = json.loads(soup.css.select('script#__NEXT_DATA__')[0].text)
        links = ['https://www.realtor.com/realestateandhomes-search/{}/'.format(permalink) for permalink in data['props']['pageProps']['properties']]
        yield data

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(RealtorspiderSpider)
    process.start()