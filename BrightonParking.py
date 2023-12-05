from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from tempfile import mkdtemp
import time
import os
import datetime as dt

LOGIN_URL = "https://reservenski.parkbrightonresort.com/login"


class BrightonParking:
    def __init__(self, driver, credentials):
        self.driver = driver
        self.driver.get(LOGIN_URL)
        self.username = credentials['username']
        self.password = credentials['password']

    def start_session(self):
        """Creates the selenium session
        """
        # Setup option
        options = Options()

        # Open
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(LOGIN_URL)

    def login(self):
        """Login the user with enviornment variables
        """
        # Get elements
        username = self.driver.find_element(By.ID, "emailAddress")
        password = self.driver.find_element(By.ID, "password")
        submit_btn = self.driver.find_element(
            By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div[2]/div/div/form/div[3]/button')

        # Fill
        # username.send_keys(os.environ['solitude_username'])
        # password.send_keys(os.environ['solitude_password'])
        username.send_keys(self.username)
        password.send_keys(self.password)

        # Submit
        submit_btn.click()

        # Wait until finished and re-directed
        WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located(
            (By.XPATH,
             '//div[text()="Reserve Parking Before Arriving at Brighton"]')
        ))

    def activate_code(self):
        """Goes to the parking code page and choose the pass option
        this will give us the $0 option in booking
        """
        # Go to codes
        self.driver.get(
            "https://reservenski.parkbrightonresort.com/parking-codes")

        # Wait for button
        btn_xpath = '//button[text()="Reserve Parking"]'
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
            (By.XPATH, btn_xpath)))

        # Select Code
        btn = self.driver.find_element(
            By.XPATH, btn_xpath)
        btn.click()

        # This will automatically navigate to calendar, just don't let
        # go until this is complete
        WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[text()="What Day Are You Parking at "]')
        ))

    def go_to_selection_calendar(self):
        """Goes to the calendar selection page, if not already there
        """
        if (self.driver.current_url != "https://reservenski.parkbrightonresort.com/select-parking"):
            self.driver.get(
                "https://reservenski.parkbrightonresort.com/select-parking")

    def navigate_to_date(self, date):
        """On the calendar selection page, ensure that the month of interest
        is in view

        Args:
            date (datetime): date we want to be able to select
        """
        # Wait for calendar to load
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'ParkingSelection_calendarWrapper__kS9AJ')))

        # Navigate to appropriate month
        self._go_to_month(date)

        # Click the date
        self._click_date(date)

    def _go_to_month(self, date):
        """Assumes already on the calendar, checks the displayed month
        and if it is not the correct month (matching date) then goes 
        FORWARD until it reaches a match

        Args:
            date (datetime): datetime with month we want to match
        """
        # Get the current month
        current_month = self.driver.find_element(
            By.CLASS_NAME, "mbsc-calendar-month").text

        target_month = date.strftime("%B")
        while current_month != target_month:
            # Click next button
            btn = self.driver.find_element(
                By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div/div[1]/div/button[3]')
            btn.click()

            # Wait until month is showing
            time.sleep(.5)
            current_month = self.driver.find_element(
                By.CLASS_NAME, "mbsc-calendar-month").text

    def _click_date(self, date):
        """Assuming that we are in the correct month
        Finds the date, and clicks it

        Args:
            date (datetime): date we want to select
        """
        # Get the matching string
        date_string = date.strftime("%A, %B %d")

        # Find the date button
        btn = self.driver.find_element(
            By.XPATH, '//div[@aria-label="{}"]'.format(date_string))
        btn.click()

        # Give it a moment to load the options
        time.sleep(.5)

    def select_parking_option(self):
        """Clicks the Season Pass Holder option once the date
        is selected, which redirect to purchasing
        """
        # Find button
        btn = self.driver.find_element(
            By.XPATH, '//div[text()="Season\'s Pass"]/parent::*/parent::*')
        btn.click()

        # Wait for honk to load
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
            (By.XPATH, '//div[text()="Checkout"]')))

    def reserve(self):
        """Once we are on honk, pull trigger and reserve the pass!
        """
        # Ensure that the button is there
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
            (By.XPATH, '//div[text()="Redeem A Pass"]')))

        # Get Button
        btn = self.driver.find_element(
            By.XPATH, '//div[text()="Redeem A Pass"]/parent::*/parent::*')
        btn.click()

        # Wait for Confirm button
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
            (By.XPATH, '//button[text()="Confirm"]')))

        # Click confirm button
        confirm_btn = self.driver.find_element(
            By.XPATH, '//button[text()="Confirm"]')
        confirm_btn.click()
        print("Reservation complete")

    def output(self):
        print(self.driver.current_url)

    def make_reservation(self, target_date):
        self.login()
        self.activate_code()
        self.go_to_selection_calendar()
        self.navigate_to_date(target_date)
        self.select_parking_option()
        self.reserve()


if __name__ == "__main__":
    options = webdriver.ChromeOptions()

    options.add_argument("--headless=new")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    chrome = webdriver.Chrome(options=options)
    sp = BrightonParking(chrome, credentials={
        'username': "amycai12@yahoo.com",
        'password': "tiphes-mozki5-rArzun"
    })
    sp.start_session()
    sp.login()
    sp.activate_code()
    sp.go_to_selection_calendar()
    sp.navigate_to_date(dt.datetime(2024, 1, 11))
    sp.select_parking_option()
    # sp.reserve()
    # Set a breakpoint here to keep page open
    print("Done")
