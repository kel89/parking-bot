import datetime

from selenium import webdriver


from honkApi import getCurrentReservations, getAvailableDates

from BrightonParking import BrightonParking
import schedule
import time

user = {
    "username": "edwardhcai@gmail.com",
    "password": "8cb!9Qh.tk"
}

# requestedDates = [datetime.date(2024, 1, 18), datetime.date(2023, 12, 9)]
requestedDates = [datetime.date(2023, 12, 8), datetime.date(2023, 12, 10)]
# requestedDates = [datetime.date(2023, 12, 9)]


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


def checkForReservations():
    global shouldUpdateCurrentReservations
    global reservedDates

    if shouldUpdateCurrentReservations:
        reservedDates = getCurrentReservations(creds=user)
        print("Updated current reservations", reservedDates)
        shouldUpdateCurrentReservations = False

    # Check dates in requestedDates but not in reservedDates
    datesToCheck = [
        date for date in requestedDates if date not in reservedDates]

    availableDates = getAvailableDates(datesToCheck)

    # Some printing to show that the script is running
    if (len(availableDates) == 0):
        print(".", end="", flush=True)
        return

    for date in availableDates:
        print("Attempting to reserve date: " + str(date))
        bp = BrightonParking(driver=chrome, credentials=user)
        try:
            bp.make_reservation(datetime.datetime(
                date.year, date.month, date.day))
            shouldUpdateCurrentReservations = True
        except Exception as e:
            print("Failed to reserve date: " + str(date))
            print(e)


if __name__ == "__main__":

    print("Attempting to reserve dates: " + str(requestedDates))

    schedule.every(30).seconds.do(checkForReservations)

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
