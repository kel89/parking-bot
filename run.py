from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
import os

HEADLESS=False

# Set Driver options
if HEADLESS:
    options = Options()
    options.add_argument("--headless=new")

# init driver
driver = webdriver.Chrome(options=options)

# Login -------
driver.get("https://reserve.altaparking.com/login")

# Get elements
username = driver.find_element(By.ID, "emailAddress")
password = driver.find_element(By.ID, "password")
submit_btn = driver.find_element(
    By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div[2]/div/div/form/div[3]/button')

# Fill
username.send_keys(os.environ['alta_username'])
password.send_keys(os.environ['alta_password'])

# Submit
submit_btn.click()
# driver.implicitly_wait(5)

# Wait for login to complete
WebDriverWait(driver, 15).until(EC.presence_of_element_located(
    (By.XPATH, '//div[text()="Reserve Parking Before Arriving at Alta"]')))

# Go to calendar
driver.get("https://reserve.altaparking.com/select-parking")

# Wait for calendar page to load
print("Waiting...")
WebDriverWait(driver, 15).until(EC.presence_of_element_located(
    (By.CLASS_NAME, 'ParkingSelection_calendarWrapper__kS9AJ')))
print("page loaded")

# Get the month
current_month = driver.find_element(By.CLASS_NAME, "mbsc-calendar-month")
print("Current Month:", current_month.text)

# Add logic to determine what date we want
while current_month.text != "January":
    # Click next button
    btn = driver.find_element(
        By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div/div[1]/div/button[3]')
    btn.click()
    # driver.implicitly_wait(5)
    time.sleep(.5)
    current_month = driver.find_element(By.CLASS_NAME, "mbsc-calendar-month")

# Find day that we want
btn = driver.find_element(By.XPATH, '//div[@aria-label="Friday, January 26"]')
btn.click()

# Now click on the paid reservation button (need a wait?)
time.sleep(.5)
btn = driver.find_element(
    By.XPATH, '//*[@id="root"]/div/div/div/div[3]/div[2]/div/div/div[1]')
btn.click()

print(driver.title)
