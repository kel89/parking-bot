from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By
from SolitudeParking import SolitudeParking
import datetime as dt

def handler(event=None, context=None):
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService("/opt/chromedriver")

    options.binary_location = '/opt/chrome/chrome'
    options.add_argument("--headless=new")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    # options.add_argument("--window-size=1280x1696")
    options.add_argument("--window-size=1280,1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")

    chrome = webdriver.Chrome(options=options, service=service)
    # chrome.get("https://example.com/")

    # return chrome.find_element(by=By.XPATH, value="//html").text
    try:
        sp = SolitudeParking(chrome)
        sp.login()
        sp.activate_code()
        sp.go_to_selection_calendar()
        sp.navigate_to_date(dt.datetime(2024, 2, 19))
        sp.select_parking_option()
        sp.reserve()
    except:
        print(chrome.page_source)


    return "hey"
