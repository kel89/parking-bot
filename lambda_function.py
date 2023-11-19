from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def lambda_handler(event, context):
    # message = 'Hello {} {}!'.format(event['first_name'], event['last_name'])  
    options = Options()
    ooptions.add_argument("window-size=1400,1200")
    options.add_argument("--headless")

    # other parameters for running headless in Lambda I used
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument("--single-process")
    options.add_argument("--user-data-dir=/tmp/chrome-user-data")
    options.add_argument("--remote-debugging-port=9222")
    print("Created options")

    # driver = webdriver.Chrome(options=options)
    driver_path = "/usr/lib/chromium-browser/chromedriver"

    # return this initialized driver
    webdriver.Chrome(
        chrome_options=options,
        executable_path=driver_path,
    )
    print("Driver init")
    driver.get("http://www.google.com")
    print("Got page")

    print("Made it here")
    print(driver.current_url)
    return { 
        'current_url' : driver.current_url
    }