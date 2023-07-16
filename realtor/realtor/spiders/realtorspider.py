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

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(BASE_DIR)

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# , meta={'proxy': env('PROXY_URL'),}

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

def extract(value):
    return value if value else None
class RealtorspiderSpider(scrapy.Spider):
    name = "realtorspider"
    allowed_domains = ["realtor.com", "localhost"]
    custom_settings={
            "PROXY_POOL_ENABLED" : True,
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "DOWNLOAD_HANDLERS": {
                "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
            "DOWNLOADER_MIDDLEWARES": {
                'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
                'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
                'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
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
        # https://www.realtor.com/realestateandhomes-detail/7309-Azimuth-Ln_Sacramento_CA_95842_M29288-48779
        url = 'https://www.realtor.com/realestateandhomes-detail/12475-State-Highway-180-Lot-37_Gulf-Shores_AL_36542_M93923-36924/'
        
        # for state in states:
        # for state in ['Alabama']:
        # category = 'rent'
        # page = random.randint(1, 5)
        # state = random.choice(states).replace(' ', '-')
        # url = f'https://www.realtor.com/{category_dict[category]}/{state}/pg-{page}'
        if 'realestateandhomes-detail' in url:
            self.logger.info('in property link = {}'.format(url))
            yield scrapy.Request(url,
                headers=headers)
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
            headers=headers)


    def parse(self, response):
        self.logger.info("Parse property function called on %s", response.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            data = json.loads(soup.css.select('script#__NEXT_DATA__')[0].text)['props']['pageProps']['property']
        except:
            delay = 5
            retry_url = response.request.url
            self.logger.info(f"Retrying {retry_url} after {delay} seconds...")
            time.sleep(delay)
            yield scrapy.Request(url=retry_url, headers=headers, meta={'retry': True})
            data = json.loads(soup.css.select('script#__NEXT_DATA__')[0].text)['props']['pageProps']['property']
        print("data", data)
        if len(data['local']) > 1:
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
        
        # for advertiser in data['consumer_advertisers']:
        #     if advertiser['type'] == 'Agent':
        #         models.Agent.objects.create(
        #             property=property,
        #             agent_id=advertiser['agent_id'],
        #         )
        #         self.logger.info('in agent link = {}'.format(advertiser['href']))
        #         yield scrapy.Request(f"https://www.realtor.com{advertiser['href']}",
        #         headers=headers,
        #         callback=self.parse_agent,}
        #         )
                
        return data
    
    # def parse_agent(self, response):
    #     self.logger.info("Parse agent function called on %s", response.url)
    #     self.logger.info("Parse property function called on %s", response.url)
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     data = json.loads(soup.css.select('script#__NEXT_DATA__')[0].text)['props']['pageProps']
    #     # agent = models.Agent.objects.get(agent_id=agent_id)
        

# def f(q, spider, page, category):
#     try:
#         settings = get_project_settings()
#         runner = CrawlerRunner(settings)
#         deferred = runner.crawl(spider, page=page, category=category)
#         deferred.addBoth(lambda _: reactor.stop())
#         reactor.run()
#         q.put(None)
#     except Exception as e:
#         q.put(e)
            
# def run_spider(spider, page, category):
#     q = Queue()
#     p = Process(target=f, args=(q,spider,page,category))
#     p.start()
#     result = q.get()
#     p.join()

#     if result is not None:
#         raise result
    
# def scrape():
#     if __name__ == "__main__":
#         process = CrawlerProcess()
#         for page in range(1, 2):
#             for category in ['buy', 'rent']:
#                 logging.info('starting')
#                 process.crawl(RealtorspiderSpider, page=page, category=category)
#                 process.start()
#         logging.info("finished")    
#     else:
#         for page in range(1, 2):
#             for category in ['buy', 'rent']:
#                 logging.info('starting')
#                 configure_logging()
#                 run_spider(RealtorspiderSpider, page=page, category=category)
#         logging.info("finished")


process = CrawlerProcess()
process.crawl(RealtorspiderSpider)
process.start()