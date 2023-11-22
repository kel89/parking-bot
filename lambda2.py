import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service







def lambda_handler(event, context):
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--user-data-dir=/tmp/chromium")
    chrome_options.add_argument("--remote-debugging-port=9222") 
    chrome_options.binary_location = '/opt/chromium/chrome'
    service = Service(executable_path='/opt/chromedriver/chromedriver')
    driver = webdriver.Chrome(
        options=chrome_options,
        service=service,
    )
    driver.get("http://www.google.com")
    print("Got page")

    print("Made it here")
    print(driver.current_url)
    return { 
        'current_url' : driver.current_url
    }