import datetime
import os

from selenium import webdriver


from honkApi import HonkApiResortClients

from BrightonParking import BrightonParking
import schedule
import time

from dotenv import load_dotenv

load_dotenv()

# requestedDates = [datetime.date(2023, 12, 8), datetime.date(2023, 12, 10)]
requestedDates = [datetime.date(2024, 1, 9)]

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

apiClient = HonkApiResortClients.BRIGHTON.value
apiClient.addCredentials({
    "username": os.getenv("USERNAME"),
    "password": os.getenv("PASSWORD")
})


def checkForReservations():
    global shouldUpdateCurrentReservations
    global reservedDates

    if shouldUpdateCurrentReservations:
        reservedDates = apiClient.getCurrentReservations()
        print("Updated current reservations", reservedDates)
        shouldUpdateCurrentReservations = False

    # Check dates in requestedDates but not in reservedDates
    datesToCheck = [
        date for date in requestedDates if date not in reservedDates]

    availableDates = apiClient.getAvailableDates(datesToCheck)

    # Some printing to show that the script is running
    if (len(availableDates) == 0):
        print(".", end="", flush=True)
        return

    for date in availableDates:
        print("Attempting to reserve date: " + str(date))
        bp = BrightonParking(driver=chrome, credentials=apiClient.creds)
        try:
            bp.make_reservation(datetime.datetime(
                date.year, date.month, date.day))
            shouldUpdateCurrentReservations = True
        except Exception as e:
            print("Failed to reserve date: " + str(date))
            print(e)


if __name__ == "__main__":
    print("Script running to reserve dates: " + str(requestedDates))

    checkForReservations()
    schedule.every(10).seconds.do(checkForReservations)

    # Loop until all dates are reserved
    while True:
        if all(date in reservedDates for date in requestedDates):
            print("All dates reserved!")
            exit(0)

        if len(reservedDates) >= 5:
            print("Reached max reservations")
            exit(0)

        schedule.run_pending()
        time.sleep(1)
