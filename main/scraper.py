# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# import time 

# op = webdriver.ChromeOptions()
# op.add_argument('headless')
# op.add_argument('--ignore-certificate-errors')
# op.add_argument('--incognito')
# driver = webdriver.Chrome(options=op)

# driver = webdriver.Chrome()

from zenrows import ZenRowsClient
from pathlib import Path
import environ
import os


# for state in ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
#   "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
#   "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
#   "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
#   "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
#   "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
#   "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
#   "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]:
    
    # driver.get("https://www.realtor.com/realestateandhomes-search/{}/".format(state.lower()))
    # property_list = driver.find_element(By.CSS_SELECTOR, 'ul[data-testid="property-list-container"]')
    # more_buttons = driver.find_elements(By.CSS_SELECTOR, 'a[aria-label="Go to next page"]')
    # for x in range(len(more_buttons)):
    # if more_buttons[x].is_displayed():
    #     driver.execute_script("arguments[0].click();", more_buttons[x])
    #     time.sleep(1)
    # page_source = driver.page_source
    # for elem in property_list:
    #     pass
    # driver.close()


import requests
# url = 'https://www.realtor.com/realestateandhomes-detail/684-Lakeland-Dr_Titus_AL_36080_M83130-83619'
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

url = 'https://www.realtor.com/realestateandhomes-detail/684-Lakeland-Dr_Titus_AL_36080_M83130-83619'
apikey = env('ZENROWS_API_KEY')
params = {
    'url': url,
    'apikey': apikey,
	'js_render': 'true',
	'wait_for': 'div.result-list',
    'autoparse': 'true',
}
response = requests.get('https://api.zenrows.com/v1/', params=params)
file_path = './detail.json' 
with open(file_path, 'w') as file:
    file.write(response.text)