import datetime
import os
from typing import Optional
import requests
import dataclasses
from enum import Enum


from dotenv import load_dotenv

load_dotenv()


@dataclasses.dataclass
class SpaceStatus:
    occupiedSpaces: int
    totalSpaces: int


@dataclasses.dataclass
class DateAvailability:
    date: datetime.date
    seasonPassStatus: SpaceStatus


class HonkApiClient:
    def __init__(self, honkGUID, zoneId, resortId, resortName):
        self.honkGUID = honkGUID
        self.zoneId = zoneId
        self.resortId = resortId
        self.resortName = resortName

    def addCredentials(self, creds):
        self.creds = creds

    # Returns a list of current reservations

    def getCurrentReservations(self) -> list[datetime.date]:

        try:
            # Make the first fetch request
            response = requests.post(f'https://platform.honkmobile.com/graphql?honkGUID={self.honkGUID}', headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://reservenski.parkbrightonresort.com/',
                'content-type': 'application/json',
                'x-authentication': '',
                'Origin': 'https://reservenski.parkbrightonresort.com',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'TE': 'trailers'
            }, json={
                'operationName': 'Login',
                'variables': {
                    'input': {
                        'emailAddress': self.creds["username"],
                        'password': self.creds["password"]
                    }
                },
                'query': 'mutation Login($input: LoginInput!) {\n  login(input: $input) {\n    userSession {\n      oaTag\n      __typename\n    }\n    errors\n    __typename\n  }\n}\n'
            })

            response.raise_for_status()

            data = response.json()
            authString = data["data"]["login"]["userSession"]["oaTag"]

            # Make another fetch request using the authString
            reservationsResponse = requests.post(f'https://platform.honkmobile.com/graphql?honkGUID={self.honkGUID}', headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://reservenski.parkbrightonresort.com/',
                'content-type': 'application/json',
                'x-authentication': authString,
                'Origin': 'https://reservenski.parkbrightonresort.com',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'TE': 'trailers'
            }, json={
                'operationName': 'ZoneParkingSessions',
                'variables': {
                    'zoneId': self.zoneId
                },
                'query': 'query ZoneParkingSessions($zoneId: ID!) {\n  zoneParkingSessions(zoneId: $zoneId) {\n    hashid\n    rateName\n    startTime\n    endTime\n    voided\n    transactionHistory {\n      id\n      total\n      __typename\n    }\n    zone {\n      zoneId\n      hashid\n      address {\n        street\n        city\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n'
            })

            reservationsResponse.raise_for_status()

            reservationsData = reservationsResponse.json()
            rawReservations = reservationsData["data"]["zoneParkingSessions"]

            # Parse the raw reservations into a list of dates, excluding voided reservations and reservations in the past
            reservations = []
            for reservation in rawReservations:
                if reservation["voided"]:
                    continue
                if datetime.datetime.strptime(reservation["endTime"], "%Y-%m-%dT%H:%M:%SZ") < datetime.datetime.now():
                    continue
                reservations.append(datetime.datetime.strptime(
                    reservation["startTime"], "%Y-%m-%dT%H:%M:%SZ").date())
            return reservations
        except requests.exceptions.RequestException as error:
            print("Error fetching reservations")
            print(error)
            raise error

    def getAvailability(self, startDate: datetime.date, endDate: datetime.date) -> list[DateAvailability]:

        # Internal function to parse the raw space status dict into a SpaceStatus object
        def parseSpaceStatus(rawSpaceStatus: Optional[dict]) -> SpaceStatus:
            if (rawSpaceStatus is None):
                return SpaceStatus(0, 0)

            return SpaceStatus(
                rawSpaceStatus["occupied_spaces"], rawSpaceStatus["total_spaces"]
            )

        # Internal function to fetch availability for a given date range, used since the API can only fetch 1 calendar year at a time.
        def _fetch(startDay: int, endDay: int, year: int) -> list[DateAvailability]:
            try:
                url = f'https://platform.honkmobile.com/graphql?honkGUID={self.honkGUID}'
                headers = {
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                    'Origin': 'https://reservenski.parkbrightonresort.com',
                    'Referer': 'https://reservenski.parkbrightonresort.com/',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'cross-site',
                    'TE': 'trailers',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
                    'content-type': 'application/json',
                    'x-authentication': '02eed7c6b23447188e5ab6bfd8831c9a'
                }

                requestData = {
                    'operationName': 'DetailedParkingAvailability',
                    'variables': {
                        'id': self.resortId,
                        'startDay': startDay,
                        'endDay': endDay,
                        'year': year
                    },
                    'query': 'query DetailedParkingAvailability($id: ID!, $startDay: Int!, $endDay: Int!, $year: Int!) {\n  detailedParkingAvailability(\n    id: $id\n    startDay: $startDay\n    endDay: $endDay\n    year: $year\n  )\n}\n'
                }

                response = requests.post(
                    url, headers=headers, json=requestData)
                response.raise_for_status()
                data = response.json()
                rawAvailableDates = data["data"]["detailedParkingAvailability"]
                # convert rawAvailableDates to a DateAvailability list; rawAvailableDates is a dict where each key is a date string
                availableDates = []
                for rawDate, rawAvailability in rawAvailableDates.items():
                    seasonPassString = "jZ3W0cN"

                    parsedDate = datetime.datetime.strptime(
                        rawDate, "%Y-%m-%dT%H:%M:%S%z").date()

                    # Here's something fun: it seems like when the API doesn't show an availibility for a certain type, it falls back to the "general" type.
                    # This might imply that at some point, Brighton decides that Season Pass availability is in the same pool as general availability?
                    # AKA for spots released early, it's split into groups of season pass and general, but for spots released later, it's just one big pool?
                    if seasonPassString not in rawAvailability:
                        parkingTypeKey = "general"
                    else:
                        parkingTypeKey = seasonPassString

                    seasonPass = parseSpaceStatus(
                        rawAvailability.get(parkingTypeKey))
                    availableDates.append(DateAvailability(
                        date=parsedDate,
                        seasonPassStatus=seasonPass)
                    )
                return availableDates
            except requests.exceptions.RequestException as error:
                print("Error fetching availability")
                print(error)
                return []

        # Chunk the date range into a dict of year -> startDay, endDay
        def daterange(startDate, emdDate):
            for n in range(int((emdDate - startDate).days)):
                yield startDate + datetime.timedelta(n)
        dateRange = {}
        for date in daterange(startDate, endDate + datetime.timedelta(days=1)):
            if date.year not in dateRange:
                dateRange[date.year] = {"startDay": date.timetuple(
                ).tm_yday, "endDay": date.timetuple().tm_yday}
            else:
                dateRange[date.year]["endDay"] = date.timetuple().tm_yday

        # Fetch availability for each year
        availability = []
        for year, dateRange in dateRange.items():
            availability += _fetch(dateRange["startDay"],
                                   dateRange["endDay"], year)
        return availability

    # Given a list of dates, returns those that are available to book
    def getAvailableDates(self, requestedDates: list[datetime.date]) -> list[datetime.date]:
        if len(requestedDates) == 0:
            return []

        minDate = min(requestedDates)
        maxDate = max(requestedDates)
        availability = self.getAvailability(minDate, maxDate)
        availableDates = []

        # Make a date: availability dict
        availabilityDict = {}
        for dateAvailability in availability:
            availabilityDict[dateAvailability.date] = dateAvailability.seasonPassStatus

        for date in requestedDates:
            if date in availabilityDict and availabilityDict[date].occupiedSpaces < availabilityDict[date].totalSpaces:
                availableDates.append(date)
        return availableDates


# example use:
# client = HonkApiResortClients.BRIGHTON.value
# client.addCredentials({username: "username", password: "password"})
# reservations = client.getCurrentReservations()
class HonkApiResortClients(Enum):
    BRIGHTON = HonkApiClient(
        honkGUID="kznloxi05aiqtplsfw2kw",
        zoneId="QPQdHW",
        resortId="rrIb",
        resortName="Brighton",
    )
    SOLITUDE = HonkApiClient(
        honkGUID="247dj8tezair8h6n5ru7pq",
        zoneId="9rwDuX",
        resortId="n6iK",
        resortName="Solitude",
    )


if __name__ == "__main__":
    # reservations = getCurrentReservations()
    # print(reservations)

    # dateAvailabilities = getAvailability(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=50))
    # for dateAvailability in dateAvailabilities:
    #     print(dateAvailability)

    client = HonkApiResortClients.SOLITUDE.value
    client.addCredentials({
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD")
    })

    requestedDates = [datetime.date(2023, 12, 8), datetime.date(
        2023, 12, 10), datetime.date(2024, 2, 8)]
    availableDates = client.getAvailableDates(requestedDates)
    print(availableDates)

    print("done")
