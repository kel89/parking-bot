from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def lambda_handler(event, context):
    # message = 'Hello {} {}!'.format(event['first_name'], event['last_name'])  
    options = Options()
    options.add_argument("--headless=new")
    print("Created options")

    driver = webdriver.Chrome(options=options)
    print("Driver init")
    driver.get("http://www.google.com")
    print("Got page")

    print("Made it here")
    print(driver.current_url)
    return { 
        'current_url' : driver.current_url
    }