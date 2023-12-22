"""
Use: python pollingRunner.py --config <configFile>
defaults to pollingConfig.json

Example config file:
{
    "resort": "solitude",
    "username": "johndeervalley@gmail.com",
    "password": "snowboarderssuck",
    "dates": [
        "2023-12-25",
        "2024-01-05",
    ]
}
"""

import datetime
import json

from argparse import ArgumentParser

from selenium import webdriver
from SolitudeParking import SolitudeParking


from honkApi import HonkApiResortClients

from BrightonParking import BrightonParking
import schedule
import time

import traceback


# Only set this to true at the beginning and if we try to make a reservation to
# avoid spamming the API
shouldUpdateCurrentReservations = True

# Keep track of the reservations the account currently has; used to
# avoid attempting to reserve a date that we already have reserved
reservedDates = []

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument('--no-sandbox')
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280x1696")


def checkForReservations():
    global shouldUpdateCurrentReservations
    global reservedDates

    if shouldUpdateCurrentReservations:
        reservedDates = apiClient.getCurrentReservations()
        print("Updated current reservations", reservedDates)
        shouldUpdateCurrentReservations = False

    # Try to reserve requested dates that are:
    #   - not already reserved
    #   - available
    datesToCheck = [
        date for date in requestedDates if date not in reservedDates]
    availableDates = apiClient.getAvailableDates(datesToCheck)

    # Some printing to show that the script is running
    if (len(availableDates) == 0):
        print(".", end="", flush=True)
        return

    # We're attempting to make reservations
    shouldUpdateCurrentReservations = True
    for date in availableDates:
        webdriver = createWebDriver()
        print("Attempting to reserve date: " + str(date))
        try:
            webdriver.make_reservation(datetime.datetime(
                date.year, date.month, date.day))
        except Exception as e:
            print("Failed to reserve date: " + str(date))
            traceback.print_exc()
        finally:
            webdriver.driver.quit()


if __name__ == "__main__":
    # Read in command line argument --config, specifying the file to read.
    # Defaults to pollingConfig.json
    parser = ArgumentParser()
    parser.add_argument("--config", default="pollingConfig.json")
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    try:
        creds = {
            "username": config["username"],
            "password": config["password"]
        }

        # Define a function to create a webdriver, so that we can create a new one
        # for each attempt at reserving.
        if config["resort"] == "brighton":
            apiClient = HonkApiResortClients.BRIGHTON.value

            def createWebDriver():
                chrome = webdriver.Chrome(options=options)
                return BrightonParking(chrome, credentials=creds)
        elif config["resort"] == "solitude":
            apiClient = HonkApiResortClients.SOLITUDE.value

            def createWebDriver():
                chrome = webdriver.Chrome(options=options)
                return SolitudeParking(chrome, credentials=creds)

        else:
            raise Exception(
                "Invalid resort specified in config, must be 'brighton' or 'solitude'")

        apiClient.addCredentials(creds)

        requestedDates: list[datetime.date] = [datetime.datetime.strptime(
            date, "%Y-%m-%d").date() for date in config["dates"]
        ]

    except Exception as e:
        print("Invalid config file: ", e)

    print("Script config")
    print("\tResort: " + apiClient.resortName)
    print("\tTarget Dates: " +
          ', '.join([date.strftime('%Y-%m-%d') for date in requestedDates])
          )
    print("\tUsername: " + apiClient.creds["username"])

    checkForReservations()
    schedule.every(10).seconds.do(checkForReservations)

    # Loop until all dates are reserved, or we reach max reservations
    while True:
        if all(date in reservedDates for date in requestedDates):
            print("All dates reserved!")
            exit(0)

        if len(reservedDates) >= 5:
            print("Reached max reservations")
            exit(0)

        schedule.run_pending()
        time.sleep(1)
