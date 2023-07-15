import scrapy
import random
import logging
import json
import scrapy
from bs4 import BeautifulSoup
from pathlib import Path
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from multiprocessing import Process, Queue



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
    allowed_domains = ["realtor.com", "localhost"]
    custom_settings={
        #  "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
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
    # if __name__ == '__main__':
    #     custom_settings["TWISTED_REACTOR"] = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

    # else:
    #     custom_settings["TWISTED_REACTOR"] = "twisted.internet.selectreactor.SelectReactor"
    
    def start_requests(self):
        category_dict = {
            'buy': 'realestateandhomes-search',
            'rent': 'apartments'   
        }
        # https://www.realtor.com/realestateandhomes-detail/7309-Azimuth-Ln_Sacramento_CA_95842_M29288-48779
        link = 'https://www.realtor.com/realestateandhomes-detail/12475-State-Highway-180-Lot-37_Gulf-Shores_AL_36542_M93923-36924/'
        self.logger.info('in property link = {}'.format(link))
        yield scrapy.Request(link,
            headers=headers,)
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

    def parse_state(self, response):
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

    

    def parse(self, response):
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
        
        # for advertiser in data['consumer_advertisers']:
        #     if advertiser['type'] == 'Agent':
        #         models.Agent.objects.create(
        #             property=property,
        #             agent_id=advertiser['agent_id'],
        #         )
        #         self.logger.info('in agent link = {}'.format(advertiser['href']))
        #         yield scrapy.Request(f"https://www.realtor.com{advertiser['href']}",
        #         headers=headers,
        #         callback=self.parse_agent,
        #         meta=dict(
        #         playwright = True,
        #         playwright_include_page = True,
        #     ))
                
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
        