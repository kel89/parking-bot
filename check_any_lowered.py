# one off script to check if parking availability has changed for any dates

import datetime
import os

from selenium import webdriver


from honkApi import DateAvailability, HonkApiClient, HonkApiResortClients

import schedule
import time

from dotenv import load_dotenv

load_dotenv()

# # Only set this to true at the beginning and if we try to make a reservation to
# avoid spamming the API
shouldUpdateCurrentReservations = True

reservedDates = []


options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument('--no-sandbox')
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280x1696")
chrome = webdriver.Chrome(options=options)


def getAvailabilities(apiClient: HonkApiClient, startDate: datetime.date, endDate: datetime.date) -> list[DateAvailability]:
    global previousAvailabilities

    currentAvailabilities = apiClient.getAvailability(startDate, endDate)
    return currentAvailabilities


def printNewOpenings(previousAvailabilities: list[DateAvailability], currentAvailabilities: list[DateAvailability], resortName: str):
    # Check to see if there are any dates with more available spots than before.

    # Create a date -> availability map for previous availabilities
    previousAvailabilitiesMap = {}
    for availability in previousAvailabilities:
        previousAvailabilitiesMap[availability.date] = availability

    # Iterate through current availabilities and check if there are more spots
    # available than before
    for availability in currentAvailabilities:
        if availability.date in previousAvailabilitiesMap:
            previousAvailability = previousAvailabilitiesMap[availability.date]
            if (
                availability.seasonPassStatus.totalSpaces != previousAvailability.seasonPassStatus.totalSpaces
                or availability.seasonPassStatus.occupiedSpaces != previousAvailability.seasonPassStatus.occupiedSpaces
            ):
                print("")
                print(f"timestamp: {datetime.datetime.now()}")
                print(
                    f"Changes found at {resortName} for date: {str(availability.date)}")
                print("\tPrevious availability: " +
                      str(previousAvailability.seasonPassStatus))
                print("\tNew availability: " +
                      str(availability.seasonPassStatus))

                if (availability.seasonPassStatus.occupiedSpaces < previousAvailability.seasonPassStatus.occupiedSpaces):
                    print("~~~~~~~~And it was an increase!~~~~~~~~~~~")

                print("")


brightonPrev = []


def checkBrighton():
    global brightonPrev

    client = HonkApiResortClients.BRIGHTON.value
    currentAvailabilities = getAvailabilities(
        client, datetime.date(2023, 12, 7), datetime.date(2024, 4, 10))
    printNewOpenings(brightonPrev, currentAvailabilities, "Brighton")
    brightonPrev = currentAvailabilities


solitudePrev = []


def checkSolitude():
    global solitudePrev

    client = HonkApiResortClients.SOLITUDE.value
    currentAvailabilities = getAvailabilities(
        client, datetime.date(2023, 12, 7), datetime.date(2024, 4, 10))
    printNewOpenings(solitudePrev, currentAvailabilities, "Solitude")
    solitudePrev = currentAvailabilities


if __name__ == "__main__":

    print("checking for diffs at brighton and solitude")

    schedule.every(30).seconds.do(checkBrighton)
    schedule.every(30).seconds.do(checkSolitude)

    checkBrighton()
    checkSolitude()

    # Loop until all dates are reserved
    while True:
        schedule.run_pending()
        time.sleep(1)
