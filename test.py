# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By

# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options

# from webdriver_manager.chrome import ChromeDriverManager
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromiumService
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.core.os_manager import ChromeType

# options = webdriver.ChromeOptions()
# options.binary_location = '/usr/lib/chromium-browser/chromedriver'
# service = webdriver.ChromeService('/usr/lib/chromium-browser/chromedriver')
# chrome = webdriver.Chrome(options=options, service=service)
# chrome = webdriver.Chrome(ChromeDriverManager().install())
# chrome = webdriver.Chrome()

# chrome = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
service = Service('/usr/bin/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument('--no-sandbox')
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280,1696")

driver = webdriver.Chrome(service=service, options=options)
driver.get('https://forums.raspberrypi.com')
print(driver.title)