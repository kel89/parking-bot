"""
Use: python webdriverPoller.py --config <configFile>
defaults to pollingConfig.json
"""

from argparse import ArgumentParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from tempfile import mkdtemp
import time
import datetime as dt

from SMSHelper import SMSHelper

from pollingConfig import ReservationType, load_json_config
from resorts import Resorts


class WebdriverPoller:
    def __init__(self, driver, credentials, resort, sms_helper=None):
        self.driver = driver
        self.username = credentials['username']
        self.password = credentials['password']
        self.resort = resort.value
        self.login_url = resort.value.base_url + "/login"
        self.parking_codes_url = resort.value.base_url + "/parking-codes"
        self.calendar_url = resort.value.base_url + "/select-parking"
        self.sms_helper = sms_helper

    def start_session(self):
        """Creates the selenium session
        """
        # Setup option
        options = Options()

        # Open
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.login_url)

    def login(self):
        """Login the user with enviornment variables
        """
        self.driver.get(self.login_url)

        # Get elements
        WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located(
            (By.ID,
             'emailAddress')
        ))
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
        WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located(
            (By.XPATH,
             f'//div[text()="{self.resort.main_screen_string}"]')
        ))

    def activate_code(self):
        """Goes to the parking code page and choose the pass option
        this will give us the $0 option in booking
        """
        # Go to codes
        self.driver.get(self.parking_codes_url)

        # Wait for button
        btn_xpath = '//button[text()="Reserve Parking"]'
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, btn_xpath)))

        # Select Code
        btn = self.driver.find_element(
            By.XPATH, btn_xpath)
        btn.click()

        # This will automatically navigate to calendar, just don't let
        # go until this is complete
        WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[text()="What Day Are You Parking at "]')
        ))

    def go_to_selection_calendar(self):
        """Goes to the calendar selection page, if not already there
        """
        if (self.driver.current_url != self.calendar_url):
            self.driver.get(self.calendar_url)

    def navigate_to_date(self, date):
        """On the calendar selection page, ensure that the month of interest
        is in view

        Args:
            date (datetime): date we want to be able to select
        """
        # Wait for calendar to load
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
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
        date_string = f'{date:%A}, {date:%B} {date.day}'

        # Find the date button. There are hidden calendar elements on the
        # page (to support the animation of switching months), so some dates
        # are duplicated. We find the first one that is enabled and click it.
        btns = self.driver.find_elements(
            By.XPATH, '//div[@aria-label="{}"]'.format(date_string)) + self.driver.find_elements(
            By.XPATH, '//div[@aria-label="Today, {}"]'.format(date_string))

        if len(btns) == 0:
            raise Exception(
                "Can't find date button for {}".format(date_string))

        for btn in btns:
            if btn.is_enabled() and btn.is_displayed() and btn.location['x'] > 0 and btn.location['y'] > 0:
                btn.click()
                break

    def select_parking_option(self, reservation_type: ReservationType):
        """Clicks the Season Pass Holder option once the date
        is selected, which redirect to purchasing
        """
        # Wait for button to load and click
        if (reservation_type == ReservationType.PASSHOLDER):
            btn_xpath = f'//div[text()="{self.resort.passholder_string}"]/parent::*/following-sibling::div[text()="$0"]/parent::*'
        elif (reservation_type == ReservationType.CARPOOL):
            btn_xpath = f'//div[text()="{self.resort.carpool_string}"]/parent::*/following-sibling::div[text()="$0"]/parent::*'
        elif (reservation_type == ReservationType.CREDITCARD):
            btn_xpath = f'//div[contains(text(), "{self.resort.creditcard_string}")]/parent::*/parent::*'
            # usinbg contains because sometimes have text like (only 2 remainig)
            # may want to consider using this structure for the other xpaths

        WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(
            (By.XPATH, btn_xpath)))
        btn = self.driver.find_element(
            By.XPATH, btn_xpath)
        btn.click()

        # Wait for honk to load
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//div[text()="Checkout"]')))

    def reserve(self, reservation_type: ReservationType):
        """Once we are on honk, pull trigger and reserve the pass!
        """
        if (reservation_type == ReservationType.PASSHOLDER):
            btn_xpath = '//div[text()="Redeem A Pass"]/parent::*/parent::*'
        elif (reservation_type == ReservationType.CARPOOL):
            btn_xpath = '//div[text()="Park For Free"]/parent::*/parent::*'
        elif (reservation_type == ReservationType.CREDITCARD):
            if (self.resort == Resorts.BRIGHTON.value):
                btn_xpath = '//div[text()="Pay $20.00 and Park"]/parent::*/parent::*'
                
            elif (self.resort == Resorts.SOLITUDE.value):
                btn_xpath = '//div[text()="Pay $35.00 and Park"]/parent::*/parent::*'
                # TODO: verify that this is the correct soli checkout text
                # I cannot becuase I don't see that option with my pass

        # Ensure that the button is there
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, btn_xpath)))

        # Get Button
        btn = self.driver.find_element(
            By.XPATH, btn_xpath)
        btn.click()

        # Wait for Confirm button
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//button[text()="Confirm"]')))

        # Click confirm button
        confirm_btn = self.driver.find_element(
            By.XPATH, '//button[text()="Confirm"]')
        confirm_btn.click()
        # Give some time for the reservation to complete
        time.sleep(3)
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

    def poll_for_reservation(self, target_date, reservation_type: ReservationType):
        """Polls for a reservation for the given date"""

        self.login()
        if (reservation_type == ReservationType.PASSHOLDER):
            self.activate_code()
        self.go_to_selection_calendar()
        self.navigate_to_date(target_date)

        # Refresh date is day after target date, unless target date is the last
        # day of the month, in which case we refresh to the previous day.
        refresh_date = target_date + dt.timedelta(days=1)
        if refresh_date.month != target_date.month:
            refresh_date = target_date - dt.timedelta(days=1)

        # Keep trying to select the parking option until it is available
        has_availability = False
        while not has_availability:
            try:
                self.select_parking_option(reservation_type)
                has_availability = True
            except Exception as e:
                # Option is still sold out, navigate to next/previous day and try again
                print("Failed attempt at", dt.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"))
                time.sleep(5)
                self.navigate_to_date(refresh_date)

                time.sleep(1)
                self.navigate_to_date(target_date)

        self.reserve(reservation_type)
        print("Reservation secured at ",
              dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if self.sms_helper:
            s = "Parking reservation at " + self.resort.name + " for " + target_date.strftime("%Y-%m-%d") + " has been secured!"
            self.sms_helper.send_message(s)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--config", default="pollingConfig.json")
    args = parser.parse_args()

    config = load_json_config(args.config)

    options = webdriver.ChromeOptions()

    options.add_argument("--headless=new")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    chrome = webdriver.Chrome(options=options)

    # Check for sms options
    # if config has smsEmail and smsPassword, then we will use the sms helper
    if SMSHelper.is_valid_config(config):
        sms_helper = SMSHelper(config)
    else:
        sms_helper = None

    sp = WebdriverPoller(chrome, credentials={
        "username": config.username,
        "password": config.password
    },
        resort=config.resort,
        sms_helper=sms_helper
    )
    sp.start_session()
    target = config.dates[0]
    sp.poll_for_reservation(
        dt.datetime(target.year, target.month, target.day),
        config.reservation_type)
    # sp.reserve()
    # Set a breakpoint here to keep page open
    print("Done")
